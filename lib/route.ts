import { NextFunction, Request, Response } from "express"

type RouteFunction = (req : Request, res : Response, next : NextFunction) => void

export const routeHandler = (fn : RouteFunction) => (
    req : Request, 
    res : Response, 
    next : NextFunction
) => {
    Promise.resolve(fn(req, res, next)).catch(next)
}