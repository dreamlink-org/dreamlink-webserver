from dreamlink.config import database_url, max_db_connections
from contextlib import contextmanager
from furl import furl
from atexit import register
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

class ParamsCollector:
    def __init__(self):
        self.params = dict()
        self._count = 0

    def __call__(self, value):
        if callable(value):
            return value(self)
        param = f"param{self._count}"
        self._count += 1
        self.params[param] = value
        return f"%({param})s"

class WrappedConnection:
    def __init__(self, conn):
        self.conn = conn

    def _execute(self, cursor, query):
        if callable(query):
            collector = ParamsCollector()
            sql = query(collector)
            cursor.execute(sql, collector.params)
        else:
            cursor.execute(query)

    def execute(self, query):
        with self.conn.cursor() as cursor:
            self._execute(cursor, query)
    
    def fetch_one(self, query):
        with self.conn.cursor(cursor_factory = DictCursor) as cursor:
            self._execute(cursor, query)
            return cursor.fetchone()

    def fetch_all(self, query):
        with self.conn.cursor(cursor_factory = DictCursor) as cursor:
            self._execute(cursor, query)
            return cursor.fetchall()

    @contextmanager
    def atomic(self):
        self.execute("BEGIN TRANSACTION")
        try:
            yield
            self.execute("COMMIT TRANSACTION")
        except Exception as err:
            self.execute("ROLLBACK TRANSACTION")
            raise err


db_url = furl(database_url)
db_pool = ThreadedConnectionPool(
    0, max_db_connections,
    dbname = db_url.path.segments[0],
    user = db_url.username,
    password = db_url.password,
    host = db_url.host,
    port = db_url.port,
    isolation_level = None
)

register(db_pool.closeall)

@contextmanager
def get_connection():
    conn = db_pool.getconn()
    try:
        conn.set_session(autocommit = True)
        yield WrappedConnection(conn)
    finally:
        db_pool.putconn(conn)
    
