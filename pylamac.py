#!/usr/bin/python

from pylama.context import Context

import sys

def run(infile, outfile):
    context = Context(myparent=None, func=None, indent=0)
    with open(infile) as f:
        lines = f.readlines()
        context.parse_buf(lines)
        #context.print_parse_tree()
        Context.variables['a'] = 42
        context.add()
        context.print_parse_tree()
    #print Context.variables
    context_class = Context.variables["Context"]
    #print context_class
    document = context_class.document

    #print document

    with open(outfile, 'w') as f:
        f.write(document)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: ./pylamac.py input.pymd output.tex"
    else:
        run(sys.argv[1], sys.argv[2])
