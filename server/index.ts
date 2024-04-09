import express, { Router } from "express"
import { authenticate, login, signUp } from "./auth"
import { downloadZone, getZones, uploadZone } from "./zone"
import { getUser, regenerateDreamCode, updatePassword } from "./user"

export const app = express()

app
    .use("/api", Router()
        .post("/sign-up", signUp)
        .post("/login", login)
        .get("/zones", getZones)
        .get("/zone/:namespace/:name/download", downloadZone)
        .use(authenticate)
        .get("/user", getUser)
        .put("/user/dream-code", regenerateDreamCode)
        .put("/user/password", updatePassword)
        .put("/zone/:namespace/:name", uploadZone)
    )