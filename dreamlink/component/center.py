from pdoo import style

@style
def center_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            justify-content: center;
        }}
    """

def center(doc):
    cls = doc.style(center_style())
    return doc.tag("div", {"class": cls})