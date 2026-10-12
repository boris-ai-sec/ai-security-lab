import json
import math
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, StrictInt


def now():
    return datetime.now(timezone.utc).isoformat()


def secret(name):
    return Path(os.environ.get('SECRET_DIR', '/run/secrets'), name).read_text().strip()


def dsn(database, role, password=None):
    from psycopg.conninfo import make_conninfo
    return make_conninfo(host=os.environ.get('PGHOST', 'pg'), port=os.environ.get('PGPORT', '5432'),
                         dbname=database, user=role, password=password or secret(role + '.pass'),
                         connect_timeout=5, options='-c statement_timeout=10000')


class Purchase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    operation_id: str = Field(min_length=1, max_length=80)
    grant_id: str = Field(min_length=1, max_length=80)
    resource: str = Field(min_length=1, max_length=80)
    supplier: str = Field(min_length=1, max_length=80)
    quantity: StrictInt = Field(gt=0, le=2**63-1)  # PostgreSQL bigint representation, not a grant limit.

    def binding(self, subject):
        return {**self.model_dump(), 'subject_id': subject}


class EventLog:
    def __init__(self, path, component, run_id):
        self.path, self.component, self.run_id = Path(path), component, run_id
        self.lock = threading.Lock()  # File records only; never protects authority admission.
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.sequence = sum(1 for _ in self.path.open(encoding='utf-8')) if self.path.exists() else 0

    def emit(self, event, **fields):
        with self.lock:
            self.sequence += 1
            with self.path.open('a', encoding='utf-8') as out:
                out.write(json.dumps(dict(timestamp=now(), component=self.component,
                                          run_id=self.run_id, sequence=self.sequence, event=event, **fields), default=str) + '\n')


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, default=str) + '\n', encoding='utf-8')


def finite_timeout(value):
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError('Timeout must be finite and positive')
    return result
