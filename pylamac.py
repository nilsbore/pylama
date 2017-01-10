#!/usr/bin/python

from pylama.common import latex
from pylama.context import Context

from code import InteractiveConsole

import sys

def run(filename):
    context = Context(parent=None, func=None, indent=None)
    with open(filename) as f:
        lines = f.readlines()
        context.parse_buf(lines)
        console = InteractiveConsole()
        context.evaluate(console)
    context = console.locals["context"]
    document = context.document
    print document

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please provide filename to compile..."
    run(sys.argv[1])
