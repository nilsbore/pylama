#!/usr/bin/python

from pylama.context import Context
#import os.path
import numpy as np

context = None

def latex(text):
    global context
    context.document.append(text)

def latexblock(blockname, full_width=False):
    global context
    print "COnttext:"
    print context
    if full_width:
        blockname.append('*')
    latex("\begin{%s}" % blockname)
    context.evaluate()
    latex("\end{%s}" % blockname)

def equation(full_width=False):
    latexblock("equation", full_width)

def cite(ref):
    latex("\cite{%s}" % ref)

def table(rows, cols, width="\textwidth", placement="t", caption="None"):

    context.cell = np.array([[Context() for r in range(0, cols)] for r in range(0, rows)], dtype=Context)

    latex("\begin{table*}[%s]" % self.placement)
    latex("\begin{tabular}{c")
    for c in range(1, cols):
        latex("|c")
    latex("}")
    context.evaluate()
    for r in self.rows:
        for c in self.cols:
            for child in context.cell[r, c].children:
                child.evaluate()
        latex("\\")
    latex("\end{tabular}")
    maybe_caption(self.caption)
    latex("\end{table*}")

def cell(r, c):
    context.parent.cell[r, c] = context

# def input(f, context):
#     if os.path(f).ext() == "pymd":
#         open f as b:
#             evaluate(b)
#     elif os.path(f).ext() == "md":
#         markdown(b)
#
# def escape(context):
#     markdown(context.text)
