import { db } from "../lib/database";
import { sign, verify } from "jsonwebtoken";
import { hash, compare } from "bcrypt";
import { randomBytes } from "crypto";
import { jwtSecret } from "../config";
import { z } from "zod";
import { routeHandler } from "../lib/route";

export const secretLength = 32
export const saltRounds = 10
export const authHeaderName = "X-DreamLink-Auth"
export const passwordRange = { min: 8, max: 100 }

export const AuthRequestSchema = z.object({
    handle : z.string().min(3).max(20),
    password: z.string().min(passwordRange.min).max(passwordRange.max)
})

type TokenPayload = {
    iat: number
    id: number
}

export const signUp = routeHandler(async (req, res) => {
    const schema = AuthRequestSchema.parse(req.body)
    const hashedPassword = await hash(schema.password, saltRounds)
    const user = await db.insertInto("user")
        .values({
            handle: schema.handle,
            password: hashedPassword,
            dream_code: await randomBytes(secretLength).toString("hex"),
            created_at: new Date(),
            min_jwt_iat: new Date()
        }).onConflict(
            oc => oc.column("handle")
                .doNothing()
        ).returning("id").executeTakeFirst()

    if (!user) {
        res.status(409).json({ error: "Handle already taken" })
        return
    }

    const payload : TokenPayload = { iat: Math.floor(Date.now() / 1000), id: user.id }
    return res.json({ token: sign(payload, jwtSecret) })
})

export const login = routeHandler(async (req, res) => {
    const schema = AuthRequestSchema.parse(req.body)

    const user = await db.selectFrom("user")
        .select(["id", "password"])
        .where("handle", "=", schema.handle)
        .executeTakeFirst()

    if(!user) {
        res.status(401).json({ error: "Incorrect handle" })
        return
    }

    if(!await compare(schema.password, user.password)) {
        res.status(401).json({ error: "Incorrect password" })
        return
    }

    res.json({
        token: sign({
            iat: Math.floor(Date.now() / 1000),
            id: user.id
        }, jwtSecret),
    })
})

export const authenticate = routeHandler(async (req, res, next) => {
    const token = req.header(authHeaderName) || ""
    const { iat, id } = verify(token, jwtSecret) as TokenPayload

    const user = await db.selectFrom("user")
        .selectAll()
        .where("id", "=", id)
        .where("min_jwt_iat", "<=", new Date(iat * 1000))
        .executeTakeFirst()

    if(!user) {
        res.status(401).json({ error: "Invalid token"})
        return
    }

    req.user = user
    next()
})