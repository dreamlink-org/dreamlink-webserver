from pdoo import style
from dreamlink.config import default_title, responsive_breakpoint

@style
def header_style():
    return lambda cls: f"""
        .{cls} {{
            width: 100%;
            display: flex;
            flex-direction:column;
            border-bottom: 1px dotted;
            margin-bottom:14px;
        }}

        @media (min-width: {responsive_breakpoint + 1}px) {{
            .{cls} {{
                display: none;
            }}
        }}
    """

@style
def header_title_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            flex-direction: row;
            font-size: 0.8rem;
            padding: 4px;
            gap: 4px;
            background-color: black;
            color: white;
        }}

        .{cls} a {{
            font-weight: bold;
            color: white;
        }}

        .{cls} a:visited {{
            color: white;
        }}
    """

@style
def header_content_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            justify-content: center;
            font-size: 0.9rem;
            padding: 4px;
            flex-wrap: wrap;
            flex-direction: row;
            gap: 4px;
        }}
    """

def header(doc, *, is_logged_in):
    header_cls = doc.style(header_style())
    title_cls = doc.style(header_title_style())
    content_cls = doc.style(header_content_style())
    with doc.tag("div", {"class" : header_cls}):
        with doc.tag("div", {"class" : title_cls}):
            with doc.tag("a", {"href": "/"}):
                doc.text(default_title)
            with doc.tag("div"):
                doc.text("|")
            with doc.tag("span"):
                doc.text("Created by the")
                with doc.tag("a", {"href": "https://lonny.io"}):
                    doc.text("Lonny Corporation")

        with doc.tag("div", {"class" : content_cls}):
            if is_logged_in:
                with doc.tag("a", {"href": "/dashboard"}):
                    doc.text("Dashboard")
                with doc.tag("div"):
                    doc.text("|")
                with doc.tag("a", {"href": "/logout"}):
                    doc.text("Logout")
            else:
                with doc.tag("a", {"href": "/login"}):
                    doc.text("Login")
                with doc.tag("div"):
                    doc.text("|")
                with doc.tag("a", {"href": "/sign-up"}):
                    doc.text("Sign Up")