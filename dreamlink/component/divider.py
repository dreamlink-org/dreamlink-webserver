from pdoo import style

@style
def divider_style():
    return lambda cls: f"""
        .{cls} {{
            width: 100%;
            border-bottom: 1px dotted;
        }}
    """

def divider(doc):
    cls = doc.style(divider_style())
    doc.tag("div", {"class": cls})
