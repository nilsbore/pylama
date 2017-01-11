from pylama.convenience import latex, maybe_caption, randomref
from pylama.context import Context
import numpy as np

latex("\usepackage{graphicx}")
latex("\usepackage{subcaption}")

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

    latex("\label{%s}" % label)
    latex("\end{figure}")

    return label

def figuretable(rows, cols, placement="t", label=None, caption=None):
    if label is None:
        label = randomref()

    Context.variables['cell'] = np.array([[Context(parent=Context.context, indent=Context.context.indent+4) for c in range(0, cols)] for r in range(0, rows)], dtype=Context)
    Context.variables['rows'] = rows
    Context.variables['cols'] = cols

    latex("\\begin{figure*}[%s]" % (placement))

    Context.context.add()

    #latex("\hline")
    for r in range(0, rows):
        for c in range(0, cols):
            Context.variables['cell'][r, c].add()
        latex("\\\\")

    if not caption is None:
        latex("\caption{%s}" % caption)

    latex("\label{%s}" % label)
    latex("\end{figure*}")

    return label

def subfigure(image, caption=None, label=None, placement="t", scale=1.0, width=None):
    if label is None:
        label = randomref()

    if width is None:
        width = str(1.0/Context.variables['cols']-0.01) + "\\textwidth"
    print "Subfigure width: " + width

    latex("\\begin{subfigure}[%s]{%s}" % (placement, width))

    Context.context.add()

    includegraphics(image, scale)

    if not caption is None:
        latex("\caption{%s}" % caption)

    latex("\label{%s}" % label)
    latex("\end{subfigure}")

    return label
