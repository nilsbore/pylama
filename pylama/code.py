from pylama.convenience import latex, latexl, latex_import, randomref
from pylama.context import Context
from pylama.bookkeeping import BookKeeping

latex_import("\usepackage{listings}")

def document_context(context, base_indent, document, show_arrows):
    indent_str = " "*(context.indent-base_indent)
    if context.function is not None:
        document += indent_str + ">"*show_arrows + context.function.rstrip().replace("\n", "\n"+indent_str+">"*show_arrows) + "\n"
    if context.text is not None:
        document += indent_str+context.text
    for child in context.children:
        document = document_context(child, base_indent, document, show_arrows)
    return document

def code(caption=None, label=None, show_arrows=True):
    if label is None:
        label = randomref()
    document = ""
    for child in Context.children:
        document = document_context(child, child.indent, document, show_arrows)
    latexl("\\begin{lstlisting}[label=%s, captionpos=b, breaklines=true, basicstyle=\scriptsize" % label)
    if caption is not None:
        latexl(", caption=%s" % caption)
        BookKeeping.add_label(label, "lstlisting")
    latex("]")
    latexl(document)
    latex("\end{lstlisting}")

    return label

def verbatim(code_string):
    latexl("\\texttt{%s}" % code_string)
