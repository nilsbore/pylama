#!/usr/bin/python

from pylama.context import Context
#import os.path
import numpy as np
import random, string

random.seed(1973)

def randomref():
   return ''.join(random.choice(string.lowercase) for i in range(5))

def ref(ref):
    latex("\\ref{%s}" % ref)

def documentclass(documenttype):
    latex("\documentclass{%s}" % documenttype)

def skip():
    pass

def latex(text):
    Context.document += text + "\n"

def latexl(text):
    Context.document += text

def latexblock(blockname, full_width=False):
    if full_width:
        blockname.append('*')
    latex("\\begin{%s}" % blockname)
    Context.context.add()
    latex("\end{%s}" % blockname)

def begin_document():
    latex("\\begin{document}")

def end_document():
    latex("\end{document}")

def equation(full_width=False):
    latexblock("equation", full_width)

def cite(ref):
    latex("\cite{%s}" % ref)

def maybe_caption(caption):
    if caption is not None:
        latex("\caption{%s}" % caption)

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

# def input(f, context):
#     if os.path(f).ext() == "pymd":
#         open f as b:
#             evaluate(b)
#     elif os.path(f).ext() == "md":
#         markdown(b)
#
# def escape(context):
#     markdown(context.text)
