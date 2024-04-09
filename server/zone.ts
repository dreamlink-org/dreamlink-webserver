import { randomBytes } from "crypto";
import { db } from "../lib/database";
import { routeHandler } from "../lib/route";
import { store } from "../lib/store";
import { z } from "zod";

const pageSize = 10
const fileKeyRandomLength = 32
const mimeType = "application/zip"

export const GetZonesRequestSchema = z.object({
    handle : z.string().min(3).max(20).optional(),
    page: z.number().int().positive().optional(),
})

export const getZones = routeHandler(async (req, res) => {
    const schema = GetZonesRequestSchema.parse(req.query)
    const page = schema.page || 0

    let partialQuery = db.selectFrom(["zone", "user"])
        .selectAll("zone")
        .select(["user.handle as user_handle"])
        .innerJoin("user", "user.id", "zone.user_id")
        .limit(pageSize + 1)
        .offset(page * pageSize)

    if(schema.handle) {
        partialQuery = partialQuery.where("user.handle", "=", schema.handle)
    }

    const zones = await partialQuery.execute()
    const hasMore = zones.length > pageSize

    res.json({
        hasMore,
        zones: zones.slice(0, pageSize).map((z) => ({
            id: z.id,
            name: z.name,
            user: {
                handle: z.user_handle
            }
        }))
    })

})

export const uploadZone = routeHandler(async (req, res) => {
    const name = `${req.params.namespace}/${req.params.name}`
    if (!name.startsWith(`@${req.user!.handle}/`)) {
        res.status(400).json({ error: "Invalid namespace" })
        return
    }

    const fileKey = `zone.${await randomBytes(fileKeyRandomLength).toString("hex")}.zip`
    await store.setData(fileKey, req)

    await db.insertInto("zone")
        .values({
            name,
            file_key: fileKey,
            user_id: req.user!.id,
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