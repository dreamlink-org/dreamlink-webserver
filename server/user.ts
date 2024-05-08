import { routeHandler } from "../lib/route";
import { z } from "zod";
import { saltRounds, secretLength } from "./auth";
import { randomBytes } from "crypto";
import { db } from "../lib/database";
import { compare, hash } from "bcrypt";
import type { User } from "../types/user";

import { passwordRange } from "./auth";

export const UserRequestSchema = z.object({
    handle: z.string(),
    dream_code: z.string()
})

export const UpdatePasswordRequestSchema = z.object({
    old_password: z.string().min(passwordRange.min).max(passwordRange.max),
    new_password: z.string().min(passwordRange.min).max(passwordRange.max)
})

const serializeUser = (user : User) => ({
    handle: user.handle,
    dream_code: user.dream_code
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
        user: { ...req.user, dream_code: newDreamCode }
    })
})

export const updatePassword = routeHandler(async (req, res) => {
    if(!req.user) {
        res.status(401).json({ error: "Unauthorized" })
        return
    }

    if(!await compare(req.user.password, req.body.old_password)) {
        res.status(400).json({ error: "Passwords don't match" })
        return
    }

    const hashedPassword = await hash(req.body.new_password, saltRounds)
    await db.updateTable("user")
        .set("password", hashedPassword)
        .where("id", "=", req.user.id)
    
    return res.json({
        user: serializeUser(req.user)
    })
})