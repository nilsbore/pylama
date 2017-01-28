from pylama.context import Context
from pylama.bookkeeping import BookKeeping
import random, string

random.seed(1973)

def text(text):
    Context.document += str(text)

def latex(text):
    Context.document += text + "\n"

def latex_import(text):
    Context.imports.append(text)
    Context.document += text + "\n"

def latexl(text):
    Context.document += text

def add_label(label, block):
    latex("\label{%s}" % label)
    BookKeeping.add_label(label, block)

def randomref():
   return ''.join(random.choice(string.lowercase) for i in range(5))

def maybe_caption(caption):
    if caption is not None:
        latex("\caption{%s}" % caption)
