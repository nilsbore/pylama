#!/usr/bin/python

from pylama.context import Context
from pylama.convenience import latex, randomref

def add():
    Context.context.add()

def make_title(title, author):
    latex("\\title{%s}" % title)
    latex("\\author{%s}" % author)
    latex("\maketitle")

def ref(ref):
    latex("\\ref{%s}" % ref)

def documentclass(documenttype):
    latex("\documentclass{%s}" % documenttype)

def comment():
    pass

def latexblock(blockname, full_width=False, label=None):
    if label is None:
        label = randomref()
    if full_width:
        blockname.append('*')
    latex("\\begin{%s}" % blockname)
    Context.context.add()
    latex("\label{%s}" % label)
    latex("\end{%s}" % blockname)
    return label

def begin_document():
    latex("\\begin{document}")

def end_document():
    latex("\end{document}")

def equation(full_width=False, label=None):
    return latexblock("equation", full_width, label)

def cite(ref):
    latex("\cite{%s}" % ref)

class section(object):

    def __init__(self, name, nesting=0):
        self.name = name
        self.nesting = nesting
        latex("\\" + "sub"*self.nesting + "section{%s}" % self.name)

    def subsection(self, name):
        return section(name, self.nesting+1)

# def input(f, context):
#     if os.path(f).ext() == "pymd":
#         open f as b:
#             evaluate(b)
#     elif os.path(f).ext() == "md":
#         markdown(b)
#
# def escape(context):
#     markdown(context.text)
