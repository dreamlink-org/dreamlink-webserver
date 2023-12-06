from pdoo import style
from dreamlink.config import responsive_breakpoint, default_title
from dreamlink.component.divider import divider

@style
def nav_column_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 24px;
            width: 256px;
        }}

        @media (max-width: {responsive_breakpoint}px) {{
            .{cls} {{
                display: none;
            }}
        }}
    """

@style
def nav_header_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .{cls} > *:first-child {{
            text-decoration: underline;
        }}

        .{cls} a {{ color: black; }}
        .{cls} a:visited {{ color: black; }}
        .{cls} > *:nth-child(2) {{ font-size: 0.8rem; }}
    """

def nav_column(doc, *, is_logged_in):
    column_cls = doc.style(nav_column_style())
    header_cls = doc.style(nav_header_style())
    with doc.tag("div", {"class" : column_cls}):
        doc.tag("img", {"src": "/assets/logo.png", "width": "256", "height": "256px"})
        with doc.tag("div", {"class" : header_cls}):
            with doc.tag("a", {"href": "/"}):
                with doc.tag("h1"):
                    doc.text(default_title)
            with doc.tag("span"):
                doc.text("Created by the")
                with doc.tag("a", {"href": "https://lonny.io"}):
                    doc.text("Lonny Corporation")
                    
        divider(doc)
                
        if is_logged_in:
            with doc.tag("a", {"href": "/dashboard"}):
                doc.text("Dashboard")
            with doc.tag("a", {"href": "/logout"}):
                doc.text("Logout")
        else:
            with doc.tag("a", {"href": "/login"}):
                doc.text("Login")
            with doc.tag("a", {"href": "/sign-up"}):
                doc.text("Sign Up")
        with doc.tag("a", {"href": "https://github.com/tlonny/dreamlink/releases"}):
            doc.text("Releases")