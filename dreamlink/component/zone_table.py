from pdoo import style
from dreamlink.config import responsive_breakpoint

@style
def zone_table_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-family: monospace;
            width: 100%;
        }}
    """

@style
def zone_row_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            flex-direction: row;
            justify-content: space-between;
        }}

        .{cls}:nth-child(odd) {{
            background-color: #F2F2F2;
        }}
    """

def zone_row(doc, *, name, processed_at):
    row_style = doc.style(zone_row_style())
    with doc.tag("div", {"class" : row_style}):
        with doc.tag("div", {}):
            doc.text(name)
        with doc.tag("div", {}):
            doc.text(processed_at.strftime("%Y-%m-%d %H:%M:%S"))

def zone_table(doc, *, zones):
    zone_cls = doc.style(zone_table_style())
    with doc.tag("div", {"class" : zone_cls}):
        for (zone_name, processed_at) in zones:
            zone_row(doc, name = zone_name, processed_at = processed_at)