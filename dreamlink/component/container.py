from pdoo import style
from contextlib import contextmanager
from dreamlink.component.header import header
from dreamlink.component.footer import footer
from dreamlink.component.nav_column import nav_column

@style
def container_style():
    return lambda cls: f"""
        .{cls} {{
            width: 100%;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
    """

@style
def container_body_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            flex-direction: row;
            flex-grow: 1;
            width: 100%;
            justify-content: center;
            height: 100%;
        }}
    """

@style
def container_body_content_style():
    return lambda cls: f"""
        .{cls} {{
            display: flex;
            height: 100%;
            flex-direction: column;
            max-width: 768px;
            width: 100%;
            padding: 24px;
            gap: 18px;
        }}
    """

@contextmanager
def container(doc, *, is_logged_in):
    container_cls = doc.style(container_style())
    body_cls = doc.style(container_body_style())
    content_cls = doc.style(container_body_content_style())
    with doc.tag("div", {"class" : container_cls}):
        header(doc, is_logged_in = is_logged_in)
        with doc.tag("div", {"class" : body_cls}):
            nav_column(doc, is_logged_in = is_logged_in)
            with doc.tag("div", {"class" : content_cls }):
                yield
        footer(doc)