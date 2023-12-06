from flask import Blueprint
from dreamlink.component.container import container
from dreamlink.component.meta import meta
from dreamlink.component.center import center
from dreamlink.component.markdown import markdown
from dreamlink.component.youtube_embed import youtube_embed
from dreamlink.config import default_title
from dreamlink.lib.db import get_connection
from dreamlink.auth import authenticate
from pdoo import Document

blueprint = Blueprint("home", __name__)

@blueprint.get("/")
def get_home():
    doc = Document()

    with doc.head:
        meta(doc, title = default_title)

    with get_connection() as conn:
        user_id = authenticate(conn)
        with doc.body:
            with container(doc, is_logged_in = user_id is not None):
                with doc.tag("h2"): 
                    doc.text("What is Dreamlink?")
                markdown(doc, markdown = "Dreamlink is a **completely free-to-play** creation/exploration game. Design and upload zones of any size with custom blocks. Connect your zones with your friends' using doors and explore a growing, seamlessly interconnected dreamscape! See for yourself:")
                with center(doc):
                    youtube_embed(doc, src =  "https://www.youtube.com/embed/P2O0sr0bnnA?si=6J5tXWD3ezkFPVNI")

        return str(doc)
    
    