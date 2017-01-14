from pylama.convenience import latex, latexl, randomref
from pylama.context import Context

latex("\usepackage{listings}")

def document_context(context, base_indent, document):
    indent_str = " "*(context.indent-base_indent)
    if context.function is not None:
        document += indent_str + ">" + context.function
    if context.text is not None:
        document += indent_str+context.text
    for child in context.children:
        document = document_context(child, base_indent, document)
    return document

def code(caption=None, label=None):
    if label is None:
        label = randomref()
    document = ""
    for child in Context.children:
        document = document_context(child, child.indent, document)
    latexl("\\begin{lstlisting}[label=%s, captionpos=b" % label)
    if caption is not None:
        latexl(", caption=%s" % caption)
    latex("]")
    latex(document)
    latex("\end{lstlisting}")
