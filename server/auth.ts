import { db } from "../lib/database";
import { JsonWebTokenError, sign, verify } from "jsonwebtoken";
import { hash, compare } from "bcrypt";
import { randomBytes } from "crypto";
import { jwtSecret } from "../env.json";
import { z } from "zod";
import { routeHandler } from "../lib/route";

export const secretLength = 32
export const saltRounds = 10
export const authHeaderName = "X-Auth"

export const AuthRequestSchema = z.object({
    handle : z.string(),
    password: z.string()
})

type TokenPayload = {
    iat: number
    id: number
}

export const signUp = routeHandler(async (req, res) => {
    const schema = AuthRequestSchema.safeParse(req.body)
    if(!schema.success) {
        res.status(400).json({ error: "Invalid request body" })
        return
    }

    const hashedPassword = await hash(schema.data.password, saltRounds)
    const user = await db.insertInto("user")
        .values({
            handle: schema.data.handle,
            password: hashedPassword,
            dream_code: await randomBytes(secretLength).toString("hex"),
            created_at: new Date().toISOString(),
            min_jwt_iat: 0
        }).onConflict(
            oc => oc.column("handle")
                .doNothing()
        ).returning("id").executeTakeFirst()

    if (!user) {
        res.status(409).json({ error: "Handle already taken" })
        return
    }

    const payload : TokenPayload = { iat: Math.floor(Date.now() / 1000), id: user.id }
    return res.json({ authToken: sign(payload, jwtSecret) })
})

export const login = routeHandler(async (req, res) => {
    const schema = AuthRequestSchema.safeParse(req.body)
    if(!schema.success) {
        res.status(400).json({ error: "Invalid request body" })
        return
    }

    const user = await db.selectFrom("user")
        .select(["id", "password"])
        .where("handle", "=", schema.data.handle)
        .executeTakeFirst()

    if(!user) {
        res.status(401).json({ error: "Incorrect handle" })
        return
    }

    if(!await compare(schema.data.password, user.password)) {
        res.status(401).json({ error: "Incorrect password" })
        return
    }

    res.json({
        authToken: sign({
            iat: Math.floor(Date.now() / 1000),
            id: user.id
        }, jwtSecret),
    })
})

export const logout = routeHandler(async (req, res) => {
    if(!req.user) {
        res.status(401).json({ error: "Unauthorized" })
        return
    }

    await db.updateTable("user")
        .set("min_jwt_iat", Math.floor(Date.now() / 1000))
        .where("id", "=", req.user.id)
        .execute()
    
    res.json({ })
})

export const authenticate = routeHandler(async (req, res, next) => {
    const token = req.header(authHeaderName) || null
    if(token === null) {
        next()
        return
    }

    let iat, id : number
    try {
        const result = verify(token, jwtSecret) as TokenPayload
        iat = result.iat
        id = result.id
    } catch(err) {
        if(err instanceof JsonWebTokenError) {
            next()
            return
        }
        throw err
    }

    const user = await db.selectFrom("user")
        .selectAll()
        .where("id", "=", id)
        .where("min_jwt_iat", "<=", iat)
        .executeTakeFirst()

    req.user = user
    next()
})