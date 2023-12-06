from flask import Blueprint, request, Response
from time import timezone
from datetime import datetime, timezone
from os.path import join
from secrets import token_hex
from dreamlink.lib.logging import log
from dreamlink.lib.db import get_connection
from dreamlink.lib.store import strategy

zone_mime_type = "application/zip"
blueprint = Blueprint("nexus", __name__)

@blueprint.get("/nexus/<string:zone_prefix>/<string:zone_suffix>")
def get_zone(zone_prefix, zone_suffix):
    with get_connection() as conn:
        file_key, = conn.fetch_one(lambda col: f"""
            SELECT file_key FROM "zone"
            WHERE "name" = {col(join(zone_prefix, zone_suffix))}
        """) or (None,)

    if file_key is None:
        return dict(
            success = False, 
            error = "Zone Missing"
        ), 404

    bytedata = strategy.get_data(file_key)
    return Response(bytedata, mimetype = zone_mime_type)

@blueprint.post("/nexus/<string:zone_prefix>/<string:zone_suffix>")
def post_zone(zone_prefix, zone_suffix):
    with get_connection() as conn:
        dream_code = request.headers.get("X-Nexus-Auth", "").replace("-", "")
        user_id, handle = conn.fetch_one(lambda col: f"""
            SELECT "id", "handle" FROM "user"
            WHERE "dream_code" = {col(dream_code)}
        """) or (None, None)

        if user_id is None:
            return dict(
                success = False, 
                error = "Invalid DreamCode"
            ), 401

        utc_now = datetime.now(timezone.utc)
        zone_key = f"zone.{token_hex(8)}.zip"

        if zone_prefix != f"@{handle}":
            return dict(
                success = False,
                error = "Invalid Zone Name"
            ), 403

        zone_id, file_key = conn.fetch_one(lambda col: f"""
            INSERT INTO "zone" (
                "user_id", "name", "file_key", "created_at", "updated_at"
            ) VALUES  (
                {col(user_id)}, 
                {col(join(zone_prefix, zone_suffix))},
                {col(zone_key)},
                {col(utc_now)},
                {col(utc_now)}
            ) ON CONFLICT ("name") DO UPDATE SET
                "updated_at" = {col(utc_now)},
                "processed_at" = NULL
            RETURNING id, file_key
        """)
        
        log(f"Zone {zone_id} uploaded by {handle}")
        strategy.set_data(file_key, request.get_data())
        conn.execute(lambda col: f"""
            UPDATE "zone" SET 
                "processed_at" = {col(datetime.now(timezone.utc))}
            WHERE "id" = {col(zone_id)}
        """)
        
        return dict(success = True)