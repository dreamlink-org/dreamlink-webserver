import { randomBytes } from "crypto";
import { db } from "../lib/database";
import { routeHandler } from "../lib/route";
import { store } from "../lib/store";
import { z } from "zod";

const pageSize = 10
const fileKeyRandomLength = 32
const mimeType = "application/zip"
const dreamCodeHeader = "X-Dream-Code".toLowerCase()

export const GetZonesRequestSchema = z.object({
    handle : z.string().optional(),
    page: z.coerce.number().int().min(0).optional(),
    maxResults: z.coerce.number().int().min(1).max(20).optional()
})

export const getZones = routeHandler(async (req, res) => {
    const schema = GetZonesRequestSchema.parse(req.query)
    const page = schema.page || 0
    const maxResults = schema.maxResults || pageSize

    let partialQuery = db.selectFrom(["zone"])
        .selectAll("zone")
        .innerJoin("user", "user.id", "zone.user_id")
        .select(["user.handle as user_handle"])
        .orderBy("zone.created_at", "desc")
        .limit(maxResults + 1)
        .offset(page * maxResults)

    if(schema.handle) {
        partialQuery = partialQuery.where("user.handle", "=", schema.handle)
    }

    const zones = await partialQuery.execute()
    const hasMore = zones.length > maxResults

    res.json({
        hasMore,
        zones: zones.slice(0, maxResults).map((z) => ({
            id: z.id,
            name: z.name,
            user: {
                id: z.user_id,
                handle: z.user_handle
            }
        }))
    })

})

export const uploadZone = routeHandler(async (req, res) => {
    const dreamCode = req.headers[dreamCodeHeader] || ""
    const user = await db.selectFrom("user")
        .selectAll()
        .where("dream_code", "=", dreamCode)
        .executeTakeFirst()
    
    if(!user) {
        res.status(401).json({ error: "Unauthorized" })
        return
    }

    const name = `${req.params.namespace}/${req.params.name}`
    if (!name.startsWith(`@${user.handle}/`)) {
        res.status(400).json({ error: "Invalid namespace" })
        return
    }

    const fileKey = `zone.${await randomBytes(fileKeyRandomLength).toString("hex")}.zip`
    await store.setData(fileKey, req)

    await db.insertInto("zone")
        .values({
            name,
            file_key: fileKey,
            user_id: user.id,
            created_at: new Date(),
            updated_at: new Date()
        }).execute()

    res.json({ })
})

export const downloadZone = routeHandler(async (req, res) => {
    const name = `${req.params.namespace}/${req.params.name}`
    const zone = await db.selectFrom("zone")
        .select("file_key")
        .where("name", "=", name)
        .executeTakeFirst()

    if(!zone) {
        res.status(404).json({ error: "Zone not found" })
        return
    }

    res.setHeader("Content-Type", mimeType)
    await store.getData(zone.file_key, res)
})