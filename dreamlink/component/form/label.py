from contextlib import contextmanager
from pdoo import style

@style
def label_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
    """

@style
def label_text_style():
    return lambda cls: f"""
        .{cls} {{
            font-size: 0.8rem;
            width: 100%;
        }}
    """

@contextmanager
def label(doc, *, text):
    label_cls = doc.style(label_style())
    text_cls = doc.style(label_text_style())
    with doc.tag("div", {"class": label_cls}):
        with doc.tag("div", {"class": text_cls}):
            doc.text(text)
        yield