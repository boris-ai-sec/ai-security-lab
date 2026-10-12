import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, Header, HTTPException

from .common import Purchase, dsn, secret


def create_app(connection_string, write_token, read_token):
    app = FastAPI()

    @app.get('/health')
    def health():
        return {'ok': True}

    def auth(value, write=False):
        allowed = {write_token} if write else {write_token, read_token}
        if value.removeprefix('Bearer ') not in allowed:
            raise HTTPException(403, 'FORBIDDEN')

    @app.post('/orders')
    def create(request: Purchase, authorization: str = Header(default='')):
        auth(authorization, write=True)
        payload = request.model_dump()
        with psycopg.connect(connection_string, autocommit=True, row_factory=dict_row) as c:
            with c.transaction():
                c.execute('INSERT INTO orders (operation_id,grant_id,resource,supplier,quantity) '
                          'VALUES (%s,%s,%s,%s,%s) ON CONFLICT (operation_id) DO NOTHING', tuple(payload.values()))
                row = c.execute('SELECT * FROM orders WHERE operation_id=%s', (request.operation_id,)).fetchone()
                if any(row[k] != v for k, v in payload.items()):
                    raise HTTPException(409, 'OPERATION_IDENTITY_CONFLICT')
        # Successful response follows durable transaction commit.
        return row

    @app.get('/orders')
    def orders(grant_id: str, authorization: str = Header(default='')):
        auth(authorization)
        with psycopg.connect(connection_string, autocommit=True, row_factory=dict_row) as c:
            rows = c.execute('SELECT * FROM orders WHERE grant_id=%s ORDER BY order_id', (grant_id,)).fetchall()
        return {'orders': rows}
    return app


def app():
    return create_app(dsn('erp', 'erp'), secret('erp.write'), secret('erp.read'))
