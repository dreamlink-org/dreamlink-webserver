from furl import furl
from flask import Blueprint, redirect, request
from bcrypt import hashpw, gensalt
from secrets import token_hex
from datetime import datetime, timezone
from pdoo import Document, style
from dreamlink.lib.jwt import create_jwt
from dreamlink.lib.logging import log
from dreamlink.lib.db import get_connection
from dreamlink.component.container import container
from dreamlink.component.center import center
from dreamlink.component.markdown import markdown
from dreamlink.component.meta import meta
from dreamlink.component.alert.error import error as form_error
from dreamlink.component.form.label import label
from dreamlink.config import default_title, secure_cookies, invite_code_required
from dreamlink.auth import authenticate

blueprint = Blueprint("sign_up", __name__)

@style
def _form_style():
    return lambda cls: f"""
        .{cls} {{
            max-width: 360px;
            width: 100%;
        }}
    """

def _get_signup(*, error = None):
    doc = Document()
    with doc.head:
        meta(doc, title=f"{default_title} | Sign Up")

    form_cls = doc.style(_form_style())
    with doc.body:
        with container(doc, is_logged_in = False):
            with doc.tag("h2"):
                doc.text("Sign up for a Dreamlink account")
            markdown(doc, markdown = "Although Dreamlink is **completely free-to-play**, an account is required to publish and consume zones. Sign up now using the form below:")
            with center(doc):
                with doc.tag("form", {"class": form_cls, "method": "POST", "action": "/sign-up"}):
                    with label(doc, text = "User Handle"):
                        doc.tag("input", {"type": "text", "name": "handle" })
                    with label(doc, text = "Password"):
                        doc.tag("input", {"type": "password", "name": "password" })
                    if invite_code_required:
                        with label(doc, text = "Invite Code"):
                            doc.tag("input", {"type": "text", "name": "invite_code" })
                    with label(doc, text = "Sign Up"):
                        with doc.tag("button", {"type": "submit", "name": "submit" }):
                            doc.text("Sign Up")
                    form_error(doc, message = error)
    return str(doc)

@blueprint.get("/sign-up")
def get_signup():
    with get_connection() as conn:
        user_id = authenticate(conn)
        if user_id is not None:
            return redirect("/dashboard")
    return _get_signup()
    
@blueprint.post("/sign-up")
def post_signup():
    handle = request.form.get("handle")
    password = request.form.get("password")
    now_utc = datetime.now(timezone.utc)

    with get_connection() as conn:
        if invite_code_required:
            invite_code = request.form.get("invite_code")
            invite_id, = conn.fetch_one(lambda col: f"""
                SELECT "id" FROM "user_invite" 
                WHERE "token" = {col(invite_code)}
                AND "consumed_at" IS NULL
                AND "expires_at" > {col(now_utc)}
            """) or (None,)

            if invite_id is None:
                err_msg = "Invalid invite code"
                return _get_signup(error = err_msg)
        else:
            invite_id = None

        handle_exists, = conn.fetch_one(lambda col: f"""
            SELECT EXISTS (
                SELECT 1 FROM "user" WHERE "handle" = {col(handle)}
            )
        """) or (None,)
        if handle_exists:
            err_msg = "User handle already taken"
            return _get_signup(error = err_msg)
        
        hash = hashpw(password.encode("utf-8"), gensalt())
        with conn.atomic():
            log(f"Creating new user with handle {handle}")
            conn.execute(lambda col: f"""
                UPDATE "user_invite" SET "consumed_at" = {col(now_utc)}
                WHERE "id" = {col(invite_id)}
            """)
            user_id, jwt_code = conn.fetch_one(lambda col: f"""
                INSERT INTO "user" (
                    "handle", "password", "dream_code", "jwt_code", "created_at"
                ) VALUES (
                    {col(handle)}, 
                    {col(hash)},
                    {col(token_hex(8))},
                    {col(token_hex(8))},
                    {col(now_utc)}
                ) RETURNING id, jwt_code
            """)

        resp = redirect("/dashboard")
        resp.set_cookie(
            "jwt", 
            create_jwt(user_id, jwt_code = jwt_code),
            domain = furl(request.url).host,
            secure=secure_cookies
        )
        return resp
