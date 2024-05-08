import { Pool } from "pg";
import { databaseURL } from "../env.json";
import { Kysely, PostgresDialect } from "kysely";
import type { DB } from "kysely-codegen";

const parsedURL = new URL(databaseURL);
export const pool = new Pool({
    user: parsedURL.username,
    host: parsedURL.hostname,
    database: parsedURL.pathname.slice(1),
    password: parsedURL.password,
    port: Number(parsedURL.port),
});

export const db = new Kysely<DB>({
    dialect: new PostgresDialect({ pool })
})
