from markdown import markdown as py_markdown

def markdown(doc, *, markdown):
    return doc.raw(py_markdown(markdown))
