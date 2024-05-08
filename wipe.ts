import { pool } from "./lib/database";

const wipe = async () => {
    const rawConnection = await pool.connect()
    await rawConnection.query("DROP SCHEMA IF EXISTS public CASCADE")
    await rawConnection.query("CREATE SCHEMA public")
    await rawConnection.query("GRANT ALL ON SCHEMA public TO postgres")
    await rawConnection.query("GRANT ALL ON SCHEMA public TO public")
    await rawConnection.release()
    await pool.end()
}

wipe()