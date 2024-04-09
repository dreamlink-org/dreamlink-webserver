import { Kysely } from "kysely"

export async function up(db: Kysely<any>): Promise<void> {
    await db.schema
        .createTable("user")
        .addColumn("id", "serial", (c) => c.primaryKey())
        .addColumn("handle", "text", (c) => c.notNull())
        .addColumn("password", "text", (c) => c.notNull())
        .addColumn("dream_code", "text", (c) => c.notNull())
        .addColumn("min_jwt_iat", "timestamp", (c) => c.notNull())
        .addColumn("created_at", "timestamp", (c) => c.notNull())
        .execute()

    await db.schema
        .createIndex("user_handle_idx")
        .on("user")
        .column("handle")
        .unique()
        .execute()

    await db.schema
        .createIndex("user_dream_code_idx")
        .on("user")
        .column("dream_code")
        .unique()
        .execute()

    await db.schema
        .createTable("zone")
        .addColumn("id", "serial", (c) => c.primaryKey())
        .addColumn("user_id", "integer", (c) => c
            .references("user.id")
            .onDelete("set null")
        )
        .addColumn("name", "text", (c) => c.notNull())
        .addColumn("file_key", "text", (c) => c.notNull())
        .addColumn("created_at", "timestamp", (c) => c.notNull())
        .addColumn("updated_at", "timestamp", (c) => c.notNull())
        .execute()

    await db.schema
        .createIndex("zone_name_idx")
        .on("zone")
        .column("name")
        .unique()
        .execute()
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable("zone").execute()
  await db.schema.dropTable("user").execute()
  await db.schema.dropTable("user_invite").execute()
}