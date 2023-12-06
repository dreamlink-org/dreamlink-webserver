from dreamlink.config import jwt_secret
from dreamlink.lib.db import get_connection
from jwt import decode, DecodeError
from flask import request

def authenticate(conn):
    # Decode JWT token from cookie to get user_id.
    try:
        jwt = request.cookies.get("jwt", "")
        decoded = decode(jwt, jwt_secret, algorithms=["HS256"])
    except DecodeError:
        return None

    # Verify user_id is valid and return user_id and handle.
    with get_connection() as conn:
        user_id, = conn.fetch_one(lambda col: f"""
            SELECT "id" FROM "user"
            WHERE "id" = {col(decoded["user_id"])}
            AND "jwt_code" = {col(decoded["jwt_code"])}
        """) or (None,)
        return user_id