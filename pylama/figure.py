from pylama.convenience import latex, latex_import, maybe_caption, randomref
from pylama.context import Context
from pylama.bookkeeping import BookKeeping
import numpy as np

latex_import("\usepackage{graphicx}")
latex_import("\usepackage{subcaption}")

def includegraphics(image, scale=1.0):
    latex("\includegraphics[scale=%f]{%s}" % (scale, image))

def figure(image, caption=None, label=None, placement="t", scale=1.0):
    if label is None:
        label = randomref()

    latex("\\begin{figure}[%s]" % (placement))

    Context.context.add()

    includegraphics(image, scale)

    if not caption is None:
        latex("\caption{%s}" % caption)
        BookKeeping.add_label(label, "figure")

    latex("\label{%s}" % label)
    latex("\end{figure}")

    return label

def figuretable(rows, cols, placement="t", label=None, caption=None):
    if label is None:
        label = randomref()

    Context.variables['cell'] = np.array([[Context(myparent=Context.context, indent=Context.context.indent+4) for c in range(0, cols)] for r in range(0, rows)], dtype=Context)

    latex("\\begin{figure*}[%s]" % (placement))

    Context.context.add()

    #latex("\hline")
    for r in range(0, rows):
        for c in range(0, cols):
            Context.variables['cell'][r, c].add()
        latex("\\\\")

    if not caption is None:
        latex("\caption{%s}" % caption)
        BookKeeping.add_label(label, "figure")

    latex("\label{%s}" % label)
    latex("\end{figure*}")

    return label

def subfigure(image, caption=None, label=None, placement="t", scale=1.0, width=None):
    if label is None:
        label = randomref()

    if width is None:
        width = str(1.0/Context.variables['cols']-0.01) + "\\textwidth"

    latex("\\begin{subfigure}[%s]{%s}" % (placement, width))

    Context.context.add()

    includegraphics(image, scale)

    if not caption is None:
        latex("\caption{%s}" % caption)

    latex("\label{%s}" % label)
    latex("\end{subfigure}")

    #BookKeeping.add_label(label, "figure") # we should get this by getting the ref of parent, i.e. figuretable
    return label
