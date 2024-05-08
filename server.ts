import { port } from "./env.json"
import { app } from "./server/index"
import { db } from "./lib/database"
import process from "process"

console.log(`Listening on port: ${port}`)
const server = app.listen(port)
server.on("close", () => db.destroy())
process.on("SIGINT", () => server.close())
