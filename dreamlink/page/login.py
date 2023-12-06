from dreamlink.component.container import container
from furl import furl
from flask import Blueprint, redirect, request
from secrets import token_hex
from bcrypt import checkpw
from datetime import datetime, timezone
from dreamlink.component.center import center
from dreamlink.component.meta import meta
from dreamlink.component.form.label import label
from dreamlink.component.alert.error import error as form_error
from dreamlink.lib.jwt import create_jwt
from dreamlink.config import default_title, secure_cookies
from dreamlink.auth import authenticate
from dreamlink.lib.db import get_connection
from pdoo import Document, style

blueprint = Blueprint("login", __name__)

@style
def _form_style():
    return lambda cls: f"""
        .{cls} {{
            max-width: 360px;
            width: 100%;
        }}
    """

def _get_login(*, error = None):
    doc = Document()
    with doc.head:
        meta(doc, title=f"{default_title} | Login")

    form_cls = doc.style(_form_style())
    with doc.body:
        with container(doc, is_logged_in = False):
            with doc.tag("h2"):
                doc.text("Login to your Dreamlink account")
            with center(doc):
                with doc.tag("form", {"class": form_cls, "method": "POST", "action": "/login"}):
                    with label(doc, text = "User Handle"):
                        doc.tag("input", {"type": "text", "name": "handle" })
                    with label(doc, text = "Password"):
                        doc.tag("input", {"type": "password", "name": "password" })
                    with label(doc, text = "Login"):
                        with doc.tag("button", {"type": "submit", "name": "submit" }):
                            doc.text("Login")
                    form_error(doc, message = error)

    return str(doc)

@blueprint.get("/login")
def get_login():
    with get_connection() as conn:
        user_id = authenticate(conn)
        if user_id is not None:
            return redirect("/dashboard")
    return _get_login()

@blueprint.post("/login")
def post_login():
    with get_connection() as conn:
        handle = request.form.get("handle", "")
        password = request.form.get("password", "")
        user_id, hashed_password, jwt_code = conn.fetch_one(lambda col: f"""
            SELECT "id", "password", "jwt_code" 
            FROM "user" WHERE "handle" = {col(handle)}
        """) or (None, None, None)

        if user_id is None:
            err_msg = "User not found"
            return _get_login(error = err_msg)
        
        if not checkpw(password.encode("utf-8"), bytes(hashed_password)):
            err_msg = "Incorrect password"
            return _get_login(error = err_msg)

        resp = redirect("/dashboard")
        resp.set_cookie(
            "jwt", 
            create_jwt(user_id, jwt_code = jwt_code),
            secure=secure_cookies,
            domain = furl(request.url).host
        )
        return resp
    
    
@blueprint.get("/logout")
def get_logout():
    with get_connection() as conn:
        user_id = authenticate(conn)
        conn.execute(lambda col: f"""
            UPDATE "user" SET "jwt_code" = {col(token_hex(8))}
            WHERE "id" = {col(user_id)}
        """)
    resp = redirect("/login")
    resp.set_cookie("jwt", 
        "", 
        expires = datetime.fromtimestamp(0, timezone.utc),
        secure = secure_cookies,
        domain = furl(request.url).host
    )
    return resp