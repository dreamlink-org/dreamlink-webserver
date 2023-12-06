from pdoo import style
from datetime import datetime

@style
def footer_style():
    return lambda cls: f"""
        .{cls} {{
            width: 100%;
            display: flex;
            margin-top:24px;
            flex-direction: row;
            justify-content: flex-start;
            background-color: black;
            color: white;
        }}
    """

@style
def footer_content_style():
    return lambda cls: f"""
        .{cls} {{
            padding: 4px;
            font-size: 0.8rem;
        }}
    """

def footer(doc):
    footer_cls = doc.style(footer_style())
    content_cls = doc.style(footer_content_style())
    with doc.tag("div", {"class" : footer_cls}):
        with doc.tag("div", {"class" : content_cls}):
            year = datetime.utcnow().year
            doc.text(f"Copright {year} - Lonny Corporation")