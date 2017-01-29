#!/usr/bin/python

from pylama.context import Context
from pylama.common import string_copy
from pylama.render import render
from pylama.bookkeeping import BookKeeping

import sys

def html_add(context):

    BookKeeping.is_used = True
    #Context.variables["BookKeeping"] = BookKeeping

    document = ('<!doctype html>\n'
                '<html lang="en">\n'
                '<head>\n'
                '    <meta charset="UTF-8">\n'
                '    <title>Test Document</title>\n'
                '</head>\n'
                '<link rel="stylesheet" href="simple.css">\n'
                '<body class="bodyclass">\n'
                '<div id="container">\n')

    for child in context.children:
        if child.function is None:
            document += '    <p>\n       '
            document += child.text + "\n"
        elif child.inline:
            string_block = Context(context, '_temp_string = string_copy()')
            string_block.children.append(child)
            string_block.evaluate()
            document += '    <p>\n       '
            print Context.variables
            document += Context.variables['_temp_string']
            document += '</p>'

        else:
            #if "import" in child.function or "documentclass" in child.function:
            if ("import" in child.function or "documentclass" in child.function) or \
               ("equation" not in child.function and "table" not in child.function and \
                "code" not in child.function and "section" not in child.function):
                child.evaluate()
            else:
                render_block = Context(context, '_temp_filename = render()')
                render_block.children.append(child)
                render_block.evaluate()
                filename = Context.variables['_temp_filename']
                document += '<br><br><img src="%s" width=500>\n' % filename

    document += ('</div>\n'
                 '</body>\n'
                 '</html>')

    with open("simple.html", 'w') as f:
        f.write(document)


def run(infile, outfile):
    context = Context(myparent=None, func=None, indent=0)
    with open(infile) as f:
        lines = f.readlines()
        context.parse_buf(lines)
        #context.add()
        html_add(context)
        #context.print_parse_tree()
    context_class = Context.variables["Context"]
    document = context_class.document

    with open(outfile, 'w') as f:
        f.write(document)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: ./pylamac.py input.pymd output.tex"
    else:
        run(sys.argv[1], sys.argv[2])
