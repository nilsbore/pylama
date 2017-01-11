#!/usr/bin/python

from pylama.common import latex
from pylama.context import Context

from code import InteractiveConsole

import sys

def run(infile, outfile):
    context = Context(parent=None, func=None, indent=0)
    with open(infile) as f:
        lines = f.readlines()
        context.parse_buf(lines)
        console = InteractiveConsole()
        context.print_parse_tree()
        Context.variables['a'] = 42
        context.add()
    #print Context.variables
    context_class = Context.variables["Context"]
    #print context_class
    document = context_class.document

    print document

    with open(outfile, 'w') as f:
        f.write(document)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Please provide filename to compile..."
    run(sys.argv[1], sys.argv[2])
