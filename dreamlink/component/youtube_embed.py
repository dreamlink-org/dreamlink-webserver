from pdoo import style

@style
def embed_wrapper_style():
    return lambda cls: f"""
        .{cls} {{
            aspect-ratio: 560/315;
            width: 100%;
            max-width: 560px;
        }}
    """

def youtube_embed(doc, *, src):
    cls = doc.style(embed_wrapper_style())
    with doc.tag("div", {"class": cls}):
        doc.tag("iframe", {
            "width": "100%",
            "height": "100%",
            "src": src,
            "frameborder": "0",
            "allow": "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        })