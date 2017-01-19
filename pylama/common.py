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

def itemize():
    return latexblock("itemize", full_width=False)

def enumerate():
    return latexblock("enumerate", full_width=False)

def item():
    latex("\item")
    Context.context.add()

def add_bibliography(bibfile, bibstyle):
    latex("\\bibliography{%s}" % bibfile)
    latex("\\bibliographystyle{%s}" % bibstyle)

def cite(ref):
    latex("\cite{%s}" % ref)

def input(infile):
    indent = Context.context.indent+4
    with open(infile) as f:
        lines = [" "*indent+line for line in f.readlines()]
        Context.context.parse_buf(lines)
        Context.context.add()

class section(object):

    def __init__(self, name, nesting=0):
        self.name = name
        self.nesting = nesting
        latex("\\" + "sub"*self.nesting + "section{%s}" % self.name)

    def subsection(self, name):
        return section(name, self.nesting+1)

class scope(object):

    def __init__(self):

        self.context = Context.context

    def add(self):

        self.context.add()

    # using this hierarchically might cause some troubles
    # but one layer should be fine
    def string(self):

        document_bkp = Context.document
        Context.document = ""
        self.context.add()

        string_bkp = Context.document
        Context.document = document_bkp

        return string_bkp


# def input(f, context):
#     if os.path(f).ext() == "pymd":
#         open f as b:
#             evaluate(b)
#     elif os.path(f).ext() == "md":
#         markdown(b)
#
# def escape(context):
#     markdown(context.text)
