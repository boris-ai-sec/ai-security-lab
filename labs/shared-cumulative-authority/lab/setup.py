"""Trusted one-shot provisioning; not imported by planner/gateway/ERP."""
import json
from pathlib import Path

import psycopg
from psycopg import sql

from .common import dsn, secret

AUTHORITY = '''
CREATE TABLE IF NOT EXISTS grants (
 grant_id text PRIMARY KEY, subject_id text NOT NULL, resource text NOT NULL,
 allowed_suppliers text[] NOT NULL, max_total_quantity bigint NOT NULL CHECK(max_total_quantity>=0),
 status text NOT NULL CHECK(status IN ('ACTIVE','INACTIVE')));
CREATE TABLE IF NOT EXISTS grant_balances (
 grant_id text PRIMARY KEY REFERENCES grants(grant_id),
 charged_quantity bigint NOT NULL DEFAULT 0 CHECK(charged_quantity>=0), revision bigint NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS operations (
 operation_id text PRIMARY KEY, grant_id text NOT NULL, subject_id text NOT NULL,
 resource text NOT NULL, supplier text NOT NULL, quantity bigint NOT NULL CHECK(quantity>0),
 decision text NOT NULL CHECK(decision IN ('ALLOW','DENY')), reason text NOT NULL,
 state text NOT NULL CHECK(state IN ('DENIED','ADMITTED_UNRESERVED','RESERVED','PENDING_RECONCILIATION','COMMITTED','RELEASED')),
 mode text NOT NULL CHECK(mode IN ('corrected','vulnerable')), observed_charged bigint NOT NULL,
 erp_order_id bigint, created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 CHECK(mode<>'corrected' OR state<>'ADMITTED_UNRESERVED'));
'''
ERP = '''
CREATE TABLE IF NOT EXISTS orders (
 order_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, operation_id text UNIQUE NOT NULL,
 grant_id text NOT NULL, resource text NOT NULL, supplier text NOT NULL,
 quantity bigint NOT NULL CHECK(quantity>0), created_at timestamptz NOT NULL DEFAULT clock_timestamp());
'''


def initialize():
    with psycopg.connect(dsn('postgres', 'admin'), autocommit=True) as c:
        for role in ('gw', 'reader', 'erp'):
            if not c.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (role,)).fetchone():
                c.execute(sql.SQL('CREATE ROLE {} LOGIN PASSWORD {}').format(sql.Identifier(role), sql.Literal(secret(role + '.pass'))))
        for database, roles in (('authority', ('gw', 'reader')), ('erp', ('erp',))):
            if not c.execute('SELECT 1 FROM pg_database WHERE datname=%s', (database,)).fetchone():
                c.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(database)))
            c.execute(sql.SQL('REVOKE CONNECT ON DATABASE {} FROM PUBLIC').format(sql.Identifier(database)))
            for role in roles:
                c.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO {}').format(sql.Identifier(database), sql.Identifier(role)))
    with psycopg.connect(dsn('authority', 'admin'), autocommit=True) as c:
        c.execute(AUTHORITY)
        c.execute('GRANT USAGE ON SCHEMA public TO gw,reader')
        c.execute('GRANT SELECT ON grants,grant_balances,operations TO gw,reader')
        c.execute('GRANT INSERT ON operations TO gw')
        c.execute('GRANT UPDATE (state,erp_order_id,updated_at) ON operations TO gw')
        c.execute('GRANT UPDATE (charged_quantity,revision) ON grant_balances TO gw')
        grant = json.loads(Path('grant.json').read_text())
        with c.transaction():
            if c.execute('SELECT count(*) FROM operations').fetchone()[0]:
                raise RuntimeError('Fresh initialization required; refuse to overwrite a used grant')
            c.execute('INSERT INTO grants VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING', tuple(grant.values()))
            c.execute('INSERT INTO grant_balances(grant_id) VALUES (%s) ON CONFLICT DO NOTHING', (grant['grant_id'],))
    with psycopg.connect(dsn('erp', 'admin'), autocommit=True) as c:
        c.execute(ERP)
        c.execute('GRANT USAGE ON SCHEMA public TO erp')
        c.execute('GRANT SELECT,INSERT ON orders TO erp')
        c.execute('GRANT USAGE,SELECT ON SEQUENCE orders_order_id_seq TO erp')


if __name__ == '__main__':
    initialize()
