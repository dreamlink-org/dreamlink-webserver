from asyncio import run
from dreamlink.lib.db import get_connection

def purge():
    with get_connection() as conn:
        conn.execute("DROP SCHEMA IF EXISTS public CASCADE")
        conn.execute("CREATE SCHEMA public")
        conn.execute("GRANT ALL ON SCHEMA public TO postgres")
        conn.execute("GRANT ALL ON SCHEMA public TO public")

if __name__ == "__main__":
    run(purge())
