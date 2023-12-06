from pdoo import style

@style
def style_shims():
    return lambda _cls: """
        body {
            margin: 0px;
            font-family: monospace;
            font-size: 1rem;
        }

        h1, h2, h3, p, ul {
            margin: 0px;
        }

        li {
            padding: 4px;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        form label {
            font-size: 0.8rem;
        }

        button, input {
            font-size: 1rem;
        }

        a:visited {
            color: blue;
        }
    """

def meta(doc, *, title = None):
    doc.style(style_shims())
    doc.tag("meta", {"name": "viewport", "content" : "width=device-width, initial-scale=1.0"})
    if title is not None:
        with doc.tag("title"):
            doc.text(title)
