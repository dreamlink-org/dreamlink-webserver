import { FileMigrationProvider, Kysely, Migrator, PostgresDialect } from "kysely"
import { db } from "./lib/database"
import { exit } from "process"
import path, { join } from "path"
import { promises as fs } from "fs"
import { rootDirectory } from "./lib/root"

const migrate = async () => {

    const migrator = new Migrator({
        db, provider: new FileMigrationProvider({
            fs, path, migrationFolder: join(rootDirectory, "migrations")            
        })
    })

    const { error } = await migrator.migrateToLatest()

    await db.destroy()

    if(error) {
        console.error(error)
        exit(1)
    }

}

migrate()
