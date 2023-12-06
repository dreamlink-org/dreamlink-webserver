from pdoo import style
from contextlib import contextmanager

@style
def info_style():
    return lambda cls: f"""
        .{cls} {{
            padding: 4px;
            background-color: #e7e6f7;
            color: #110d5e;
            border: 1px dashed #110d5e;
        }}
    """

@contextmanager
def info_wrapper(doc):
    cls = doc.style(info_style())
    with doc.tag("div", {"class" : cls}):
        yield

def info(doc, *, message):
    if message is not None:
        with info_wrapper(doc):
            doc.text(message)