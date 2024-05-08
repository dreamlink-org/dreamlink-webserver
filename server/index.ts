import express, { json } from "express"
import cors from "cors"
import { authenticate, login, signUp } from "./auth"
import { downloadZone, getZones, uploadZone } from "./zone"
import { getUser, regenerateDreamCode, updatePassword } from "./user"

export const app = express()
    .use(cors())
    .use(authenticate)
    .use(json())
    .post("/sign-up", signUp)
    .post("/login", login)
    .get("/zones", getZones)
    .get("/zone/:namespace/:name/download", downloadZone)
    .get("/user", getUser)
    .put("/user/dream-code", regenerateDreamCode)
    .put("/user/password", updatePassword)
    .put("/zone/:namespace/:name", uploadZone)