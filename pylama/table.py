from pylama.context import Context
from pylama.convenience import randomref, maybe_caption, latex, latexl
import numpy as np

def table(rows, cols, width="\textwidth", placement="t", caption=None, label=None):

    if label is None:
        label = randomref()

    Context.variables['cell'] = np.array([[Context(parent=Context.context, indent=Context.context.indent+4) for c in range(0, cols)] for r in range(0, rows)], dtype=Context)
    Context.variables['rows'] = rows
    Context.variables['cols'] = cols

    latex("\\begin{table*}[%s]" % placement)
    Context.context.add()
    latexl("\\begin{tabular}{|c")
    for c in range(1, cols):
        latexl("|c")
    latex("|}")

    #context.evaluate()
    latex("\hline")
    for r in range(0, rows):
        for c in range(0, cols):
            Context.variables['cell'][r, c].add()
            if c < cols-1:
                latexl("&")
        latex("\\\\ \hline")
    latex("\end{tabular}")
    maybe_caption(caption)
    latex("\label{%s}" % label)
    latex("\end{table*}")

    return label

def setcell(r, c):
    Context.variables['cell'][r, c] = Context.context
