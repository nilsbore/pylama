#!/usr/bin/python

from pylama.context import Context
from pylama.convenience import latex

def ref(ref):
    latex("\\ref{%s}" % ref)

def documentclass(documenttype):
    latex("\documentclass{%s}" % documenttype)

def skip():
    pass

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

# def input(f, context):
#     if os.path(f).ext() == "pymd":
#         open f as b:
#             evaluate(b)
#     elif os.path(f).ext() == "md":
#         markdown(b)
#
# def escape(context):
#     markdown(context.text)
