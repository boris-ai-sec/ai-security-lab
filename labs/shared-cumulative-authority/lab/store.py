import psycopg
from psycopg.rows import dict_row

from .common import now

BOUND = ('operation_id', 'grant_id', 'subject_id', 'resource', 'supplier', 'quantity')
CHARGED = ('RESERVED', 'PENDING_RECONCILIATION', 'COMMITTED')


class IdentityConflict(Exception):
    pass


def match(row, binding):
    if any(row[k] != binding[k] for k in BOUND):
        raise IdentityConflict('OPERATION_IDENTITY_CONFLICT')


class Store:
    def __init__(self, connection_string, log, before_commit=None):
        self.dsn, self.log, self.before_commit = connection_string, log, before_commit

    def connect(self):
        return psycopg.connect(self.dsn, autocommit=True, row_factory=dict_row)

    def get(self, operation_id):
        with self.connect() as c:
            return c.execute('SELECT * FROM operations WHERE operation_id=%s', (operation_id,)).fetchone()

    def snapshot(self, grant_id):
        with self.connect() as c:
            return c.execute('SELECT g.*, b.charged_quantity, b.revision FROM grants g '
                             'JOIN grant_balances b USING(grant_id) WHERE grant_id=%s', (grant_id,)).fetchone()

    @staticmethod
    def reason(grant, binding, used):
        if grant is None:
            return 'DENY_UNKNOWN_GRANT'
        if binding['subject_id'] != grant['subject_id']:
            return 'DENY_SUBJECT_NOT_IN_GRANT'
        if grant['status'] != 'ACTIVE':
            return 'DENY_GRANT_INACTIVE'
        if binding['resource'] != grant['resource']:
            return 'DENY_RESOURCE_NOT_IN_GRANT'
        if binding['supplier'] not in grant['allowed_suppliers']:
            return 'DENY_SUPPLIER_NOT_IN_GRANT'
        if used + binding['quantity'] > grant['max_total_quantity']:
            return 'DENY_CAPACITY'
        return 'ALLOW'

    def admit(self, binding, mode, observed=None):
        # The unlocked vulnerable read happens outside this function and before the scheduling hook.
        try:
            with self.connect() as c:
                with c.transaction():
                    if mode == 'corrected':
                        balance = c.execute('SELECT * FROM grant_balances WHERE grant_id=%s FOR UPDATE',
                                            (binding['grant_id'],)).fetchone()
                        grant = c.execute('SELECT * FROM grants WHERE grant_id=%s',
                                          (binding['grant_id'],)).fetchone()
                        used = balance['charged_quantity'] if balance else 0
                    else:
                        grant = observed
                        used = observed['charged_quantity'] if observed else 0
                    existing = c.execute('SELECT * FROM operations WHERE operation_id=%s',
                                         (binding['operation_id'],)).fetchone()
                    if existing:
                        match(existing, binding)
                        return existing, False
                    reason = self.reason(grant, binding, used)
                    allowed = reason == 'ALLOW'
                    state = ('RESERVED' if mode == 'corrected' else 'ADMITTED_UNRESERVED') if allowed else 'DENIED'
                    row = c.execute('INSERT INTO operations '
                                    '(operation_id,grant_id,subject_id,resource,supplier,quantity,decision,reason,state,mode,observed_charged) '
                                    'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *',
                                    tuple(binding[k] for k in BOUND) +
                                    ('ALLOW' if allowed else 'DENY', reason, state, mode, used)).fetchone()
                    after = used
                    if allowed and mode == 'corrected':
                        after = c.execute('UPDATE grant_balances SET charged_quantity=charged_quantity+%s, '
                                          'revision=revision+1 WHERE grant_id=%s RETURNING charged_quantity',
                                          (binding['quantity'], binding['grant_id'])).fetchone()['charged_quantity']
                    if self.before_commit:
                        self.before_commit()
                # Reached only after transaction COMMIT completed successfully.
            self.log.emit('decision', operation_id=row['operation_id'], grant_id=row['grant_id'],
                          decision=row['decision'], reason=reason, state=state, observed_charged=used,
                          charged_after=after if mode == 'corrected' else None,
                          admission_consumes_capacity=allowed and mode == 'corrected', commit_confirmed=True)
            return row, True
        except psycopg.errors.UniqueViolation:
            existing = self.get(binding['operation_id'])
            if not existing:
                raise
            match(existing, binding)
            return existing, False

    def transition(self, operation_id, target, order=None, *, undispatched_proof=False):
        # No general closure subsystem. Only the owning, never-dispatched test path can request release.
        with self.connect() as c:
            with c.transaction():
                first = c.execute('SELECT * FROM operations WHERE operation_id=%s', (operation_id,)).fetchone()
                if first is None:
                    raise ValueError('Unknown operation')
                balance = c.execute('SELECT * FROM grant_balances WHERE grant_id=%s FOR UPDATE',
                                    (first['grant_id'],)).fetchone()
                row = c.execute('SELECT * FROM operations WHERE operation_id=%s FOR UPDATE', (operation_id,)).fetchone()
                previous, delta = row['state'], 0
                if target == 'COMMITTED':
                    if order is None:
                        raise ValueError('Durable matching order required')
                    for k in ('operation_id', 'grant_id', 'resource', 'supplier', 'quantity'):
                        if order[k] != row[k]:
                            raise IdentityConflict('ERP_EVIDENCE_MISMATCH')
                    if previous == 'COMMITTED':
                        self.log.emit('completion_noop', operation_id=operation_id, state=previous)
                        return row
                    if previous not in ('RESERVED', 'PENDING_RECONCILIATION', 'ADMITTED_UNRESERVED'):
                        raise ValueError('Invalid commit transition')
                    if previous == 'ADMITTED_UNRESERVED':
                        delta = row['quantity']  # No grant-limit decision after the external effect.
                elif target == 'PENDING_RECONCILIATION':
                    if previous in ('COMMITTED', 'RELEASED', 'DENIED', 'PENDING_RECONCILIATION', 'ADMITTED_UNRESERVED'):
                        return row
                    if previous != 'RESERVED':
                        raise ValueError('Invalid unknown transition')
                elif target == 'RELEASED':
                    if previous == 'RELEASED':
                        return row
                    if previous != 'RESERVED' or not undispatched_proof:
                        raise ValueError('Only definite, closed, never-dispatched execution can be released')
                    delta = -row['quantity']
                else:
                    raise ValueError('Unsupported transition')
                if delta:
                    c.execute('UPDATE grant_balances SET charged_quantity=charged_quantity+%s, '
                              'revision=revision+1 WHERE grant_id=%s', (delta, row['grant_id']))
                row = c.execute('UPDATE operations SET state=%s,erp_order_id=%s,updated_at=%s '
                                'WHERE operation_id=%s RETURNING *',
                                (target, order['order_id'] if order else row['erp_order_id'], now(), operation_id)).fetchone()
                after = balance['charged_quantity'] + delta
        self.log.emit('transition', operation_id=operation_id, previous=previous, state=target,
                      charged_before=balance['charged_quantity'], charged_after=after, commit_confirmed=True)
        return row
