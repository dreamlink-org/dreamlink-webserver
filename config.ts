import { env } from "process"

if(typeof env.DATABASE_URL === "undefined") {
    throw new Error("DATABASE_URL is not defined")
}

export const databaseURL = env.DATABASE_URL

if(typeof env.JWT_SECRET === "undefined") {
    throw new Error("JWT_SECRET is not defined")
}

export const jwtSecret = env.JWT_SECRET

if(typeof env.STORE_URI === "undefined") {
    throw new Error("STORE_URI is not defined")
}

export const storeURI = env.STORE_URI

if(typeof env.PORT === "undefined") {
    throw new Error("PORT is not defined")
}

export const port = parseInt(env.PORT)