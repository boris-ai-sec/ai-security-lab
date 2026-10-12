import asyncio
import time

from .common import finite_timeout


class InvalidSchedule(Exception):
    pass


class Barrier:
    def __init__(self, participants, timeout, log, hook):
        self.expected = set(participants)
        self.timeout = finite_timeout(timeout)
        self.log, self.hook = log, hook
        self.arrived, self.event, self.broken = set(), asyncio.Event(), False
        self.started = time.monotonic()
        log.emit('configured', participants=sorted(self.expected), timeout=self.timeout, hook=hook)

    async def wait(self, operation_id, attempt_id, observed=None):
        if operation_id not in self.expected or operation_id in self.arrived:
            self.broken = True
            self.event.set()
            self.log.emit('invalid', operation_id=operation_id, reason='unexpected_or_duplicate_participant')
            raise InvalidSchedule('INVALID_INSTRUMENTED_RUN')
        self.arrived.add(operation_id)
        self.log.emit('arrival', operation_id=operation_id, attempt_id=attempt_id,
                      observed_charged=observed['charged_quantity'] if observed else None,
                      revision=observed['revision'] if observed else None, hook=self.hook)
        if self.arrived == self.expected:
            self.log.emit('release', participants=sorted(self.arrived),
                          elapsed_seconds=time.monotonic() - self.started, hook=self.hook)
            self.event.set()
        try:
            await asyncio.wait_for(self.event.wait(), self.timeout)
        except TimeoutError:
            self.broken = True
            self.event.set()
            self.log.emit('timeout', operation_id=operation_id, classification='INVALID_INSTRUMENTED_RUN')
        if self.broken:
            raise InvalidSchedule('INVALID_INSTRUMENTED_RUN')
