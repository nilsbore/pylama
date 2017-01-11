#!/usr/bin/python

from pylama.context import Context
#import os.path
import numpy as np

def latex(text):
    Context.document += text + "\n"

def latexl(text):
    Context.document += text

def latexblock(blockname, full_width=False):
    if full_width:
        blockname.append('*')
    latex("\\begin{%s}" % blockname)
    Context.context.evaluate_children()
    latex("\end{%s}" % blockname)

def equation(full_width=False):
    latexblock("equation", full_width)

def cite(ref):
    latex("\cite{%s}" % ref)

def maybe_caption(caption):
    if caption is not None:
        latex("\caption{%s}" % caption)

def table(rows, cols, width="\textwidth", placement="t", caption="None"):

    Context.variables['cell'] = np.array([[Context(parent=Context.context, indent=Context.context.indent+4) for c in range(0, cols)] for r in range(0, rows)], dtype=Context)
    Context.variables['rows'] = rows
    Context.variables['cols'] = cols

    latex("\\begin{table*}[%s]" % placement)
    latexl("\\begin{tabular}{c")
    for c in range(1, cols):
        latexl("|c")
    latex("}")
    Context.context.evaluate_children()
    #context.evaluate()
    for r in range(0, rows):
        for c in range(0, cols):
            Context.variables['cell'][r, c].evaluate_children()
            latexl("&")
        latex("\\\\")
    latex("\end{tabular}")
    maybe_caption(caption)
    latex("\end{table*}")

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
