from pdoo import style

@style
def error_style():
    return lambda cls: f"""
        .{cls} {{
            padding: 4px;
            background-color: #fcdee1;
            color: #750b15;
            border: 1px dashed #750b15;
        }}
    """

def error(doc, *, message):
    if message is not None:
        cls = doc.style(error_style())
        with doc.tag("div", {"class" : cls}):
            doc.text(message)