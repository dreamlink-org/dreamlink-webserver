import { routeHandler } from "../lib/route";
import { z } from "zod";
import { saltRounds, secretLength } from "./auth";
import { randomBytes } from "crypto";
import { db } from "../lib/database";
import { compare, hash } from "bcrypt";
import type { User } from "../types/user";

export const UpdatePasswordRequestSchema = z.object({
    oldPassword: z.string(),
    newPassword: z.string()
})

const serializeUser = (user : User) => ({
    handle: user.handle,
    dreamCode: user.dream_code
})

export const getUser = routeHandler(async (req, res) => {
    if(!req.user) {
        res.status(401).json({ error: "Unauthorized" })
        return
    }

    res.json({
        user: serializeUser(req.user)
    })
})

export const regenerateDreamCode = routeHandler(async (req, res) => {
    if(!req.user) {
        res.status(401).json({ error: "Unauthorized" })
        return
    }

    const newDreamCode = await randomBytes(secretLength).toString("hex")
    await db.updateTable("user")
        .set("dream_code", newDreamCode)
        .where("id", "=", req.user.id)
        .execute()

    res.json({
        user: serializeUser({ ...req.user, dream_code: newDreamCode })
    })
})

export const updatePassword = routeHandler(async (req, res) => {
    if(!req.user) {
        res.status(401).json({ error: "Unauthorized" })
        return
    }

    const parsedBody = UpdatePasswordRequestSchema.safeParse(req.body)
    if(!parsedBody.success) {
        res.status(400).json({ error: "Invalid request body" })
        return
    }

    if(!await compare(parsedBody.data.oldPassword, req.user.password)) {
        res.status(400).json({ error: "Incorrect Password" })
        return
    }

    const hashedPassword = await hash(parsedBody.data.newPassword, saltRounds)
    await db.updateTable("user")
        .set("password", hashedPassword)
        .where("id", "=", req.user.id)
        .execute()
    
    return res.json({
        user: serializeUser(req.user)
    })
})