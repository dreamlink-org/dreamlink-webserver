from datetime import datetime
from dreamlink.lib.db import get_connection

from dreamlink.migration import (
    m20231205_01_init
)

migrations = [
    m20231205_01_init
]

def migrate():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS "_migration" (
                "id" SERIAL,
                "name" TEXT NOT NULL,
                "migrated_at" TIMESTAMP NOT NULL,
                PRIMARY KEY("id")
            )
        """)

        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS "_migration_name_idx" ON "_migration" ("name")
        """)

        for migration in migrations:
            with conn.atomic():
                migration_exists, = conn.fetch_one(lambda col: f"""
                    SELECT EXISTS (
                        SELECT 1 FROM "_migration"
                        WHERE "name" = {col(migration.__name__)}
                    )
                """)

                if migration_exists:
                    continue

                migration.migrate(conn)
                conn.execute(lambda col: f"""
                    INSERT INTO "_migration" (
                        name, migrated_at
                    ) VALUES (
                        {col(migration.__name__)},
                        {col(datetime.utcnow())}
                    )
                """)

if __name__ == "__main__":
    migrate()
