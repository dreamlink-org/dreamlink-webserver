
def create_user_table(conn):
    conn.execute("""
        CREATE TABLE "user" (
            "id" SERIAL,
            "handle" TEXT NOT NULL,
            "password" BYTEA NOT NULL,
            "dream_code" TEXT NOT NULL,
            "jwt_code" TEXT NOT NULL,
            "created_at" TIMESTAMP NOT NULL,
            PRIMARY KEY("id")
        )
    """)

    conn.execute("""
        CREATE UNIQUE INDEX "user_handle_idx" ON "user" ("handle")
    """)

    conn.execute("""
        CREATE UNIQUE INDEX "user_dream_code_idx" ON "user" ("dream_code")
    """)

def create_user_invite_token_table(conn):
    conn.execute("""
        CREATE TABLE "user_invite" (
            "id" SERIAL,
            "token" TEXT NOT NULL,
            "created_at" TIMESTAMP NOT NULL,
            "expires_at" TIMESTAMP NOT NULL,
            "consumed_at" TIMESTAMP NULL,
            PRIMARY KEY("id")
        )
    """)

    conn.execute("""
        CREATE UNIQUE INDEX "user_invite_token_idx" ON "user_invite" ("token")
    """)

def create_zone_table(conn):
    conn.execute("""
        CREATE TABLE "zone" (
            "id" SERIAL,
            "user_id" INTEGER NOT NULL,
            "name" TEXT NOT NULL,
            "file_key" TEXT NULL,
            "created_at" TIMESTAMP NOT NULL,
            "updated_at" TIMESTAMP NOT NULL,
            "processed_at" TIMESTAMP NULL,
            PRIMARY KEY("id"),
            FOREIGN KEY ("user_id") REFERENCES "user" ("id")
        )
    """)

    conn.execute("""
        CREATE UNIQUE INDEX "zone_name_idx" ON "zone" ("name")
    """)

def migrate(conn):
    create_user_invite_token_table(conn)
    create_user_table(conn)
    create_zone_table(conn)
