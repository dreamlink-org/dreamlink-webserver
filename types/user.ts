export type User = {
    id: number
    handle: string
    password: string
    dream_code: string
    created_at: Date,
    min_jwt_iat: Date
}