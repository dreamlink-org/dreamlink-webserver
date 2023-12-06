from bcrypt import hashpw, gensalt
from flask import Blueprint, redirect, request
from secrets import token_hex
from dreamlink.component.container import container
from dreamlink.auth import authenticate
from dreamlink.component.meta import meta
from dreamlink.component.center import center
from dreamlink.component.alert.error import error as form_error
from dreamlink.component.form.label import label
from dreamlink.component.markdown import markdown
from dreamlink.component.zone_table import zone_table
from dreamlink.config import default_title
from dreamlink.component.divider import divider
from dreamlink.lib.db import get_connection
from pdoo import Document, style

blueprint = Blueprint("dashboard", __name__)

@style
def _form_style():
    return lambda cls: f"""
        .{cls} {{
            max-width: 360px;
            width: 100%;
        }}
    """

@style
def _dream_code_value_style():
    return lambda cls: f"""
        .{cls} {{
            padding: 4px;
            border: 1px dotted;
            font-weight: bold;
            text-align: center;
            border-radius: 4px;
        }}
    """

def _get_dashboard(conn, *, user_id, password_error = None):
    handle, dream_code = conn.fetch_one(lambda col: f"""
        SELECT "handle", "dream_code" FROM "user"
        WHERE "id" = {col(user_id)}
    """)

    zones = conn.fetch_all(lambda col: f"""
        SELECT "name", "processed_at" FROM "zone"
        WHERE "user_id" = {col(user_id)}
    """)

    doc = Document()
    with doc.head:
        meta(doc, title=f"{default_title} | dashboard")
    
    dream_code_cls = doc.style(_dream_code_value_style())
    form_cls = doc.style(_form_style())
    with doc.body:
        with container(doc, is_logged_in = True):
            with doc.tag("h2"):
                doc.text(f"Welcome back, {handle}!")
            markdown(doc, markdown = "Welcome back to Dreamlink! Your dashboard is where you can manage your account, view your zones, and more.")
            divider(doc)
            if len(zones) > 0:
                with doc.tag("h2"):
                    doc.text("Your zones")
                zone_table(doc, zones = zones)
                divider(doc)
            with doc.tag("h2"):
                doc.text("Dream Code")
            markdown(doc, markdown = "It is important you **don't share** your dream code with anyone! If your dream code has been compromised, please regenerate it using the form below:")
            with center(doc):
                with doc.tag("form", {"class": form_cls, "method": "POST", "action": "/dashboard"}):
                    doc.tag("input", {"type": "hidden", "name": "action", "value": "regenerate_dream_code"})
                    with label(doc, text = "Dream Code"):
                        with doc.tag("div", {"class": dream_code_cls}):
                            doc.text(dream_code)
                    with label(doc, text = "Regenerate"):
                        with doc.tag("button", {"type": "submit", "name": "submit"}):
                            doc.text("Regenerate")
            divider(doc)
            with doc.tag("h2"):
                doc.text("Password")

            markdown(doc, markdown = "You can change your password using the form below.")
            with center(doc):
                with doc.tag("form", {"class": form_cls, "method": "POST", "action": "/dashboard"}):
                    doc.tag("input", {"type": "hidden", "name": "action", "value": "change_password"})
                    with label(doc, text = "Password"):
                        doc.tag("input", {"type": "password", "name": "password" })
                    with label(doc, text = "Password (Confirm)"):
                        doc.tag("input", {"type": "password", "name": "password_confirm" })
                    with label(doc, text = "Change"):
                        with doc.tag("button", {"type": "submit", "name": "submit" }):
                            doc.text("Change Password")

                    form_error(doc, message = password_error)
    return str(doc)

@blueprint.get("/dashboard")
def get_dashboard():
    with get_connection() as conn: 
        user_id = authenticate(conn)
        if user_id is None:
            return redirect("/login")
        else:
            return _get_dashboard(conn, user_id = user_id)

@blueprint.post("/dashboard")
def post_dashboard():
    with get_connection() as conn: 
        user_id = authenticate(conn)
        action = request.form.get("action")
        if action == "regenerate_dream_code":
            dream_code = token_hex(8)
            conn.execute(lambda col: f"""
                UPDATE "user" SET "dream_code" = {col(dream_code)}
                WHERE "id" = {col(user_id)}
            """)
        elif action == "change_password":
            password = request.form.get("password")
            password_confirm = request.form.get("password_confirm")
            if password != password_confirm:
                return _get_dashboard(
                    conn,
                    user_id = user_id, 
                    password_error = "Passwords do not match"
                )
            hashed = hashpw(password.encode("utf-8"), gensalt())
            conn.execute(lambda col: f"""
                UPDATE "user" SET "password" = {col(hashed)}
                WHERE "id" = {col(user_id)}
            """)

        return _get_dashboard(conn, user_id = user_id)