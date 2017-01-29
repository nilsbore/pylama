#!/usr/bin/python

from pylama.context import Context
from pylama.common import string_copy
from pylama.render import render
from pylama.bookkeeping import BookKeeping
import subprocess

import sys

def latex_string_to_html(string):

    args = ['pandoc', '--from=latex', '--to=html']

    p = subprocess.Popen(args, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    try:
        stdout, stderr = p.communicate(string)
    except OSError:
        # this is happening only on Py2.6 when pandoc dies before reading all
        # the input. We treat that the same as when we exit with an error...
        raise RuntimeError('Pandoc died with exitcode "%s" during conversion.' % (p.returncode))

    try:
        stdout = stdout.decode('utf-8')
    except UnicodeDecodeError:
        # this shouldn't happen: pandoc more or less garantees that the output is utf-8!
        raise RuntimeError('Pandoc output was not utf-8.')

    return stdout

def html_add(context):

    BookKeeping.is_used = True

    document = ('<!doctype html>\n'
                '<html lang="en">\n'
                '<head>\n'
                '    <meta charset="UTF-8">\n'
                '    <title>Test Document</title>\n'
                '</head>\n'
                '<link rel="stylesheet" href="styles/default_latex.css">\n'
                '<body class="bodyclass">\n'
                '<div id="container">\n')

    active = False
    tag_open = False
    #break_string = "\n    <br/>\n    <br/>\n    "
    active_paragraph = ""

    for child in context.children:
        if child.function is None:
            child.evaluate()
            active_paragraph += child.text
        elif child.inline:
            string_block = Context(context, '_temp_string = string_copy()')
            string_block.children.append(child)
            string_block.evaluate()
            active_paragraph += Context.variables['_temp_string']
        else:
            if "begin_document" in child.function:
                active = True
                child.evaluate()
                if "title" in Context.variables:
                    document += '<h1 align="center">' + Context.variables["title"] + '</h1>\n'
                if "author" in Context.variables:
                    document += '<h3 align="center">' + Context.variables["author"] + '</h3>\n'
            elif active and "end_document" in child.function:
                active = False
                child.evaluate()
            elif active:
                if len(active_paragraph) > 0:
                    document += latex_string_to_html(active_paragraph)
                    active_paragraph = ""
                render_block = Context(context, '_temp_filename = render()')
                render_block.children.append(child)
                render_block.evaluate()
                filename = Context.variables['_temp_filename']
                if filename is not None:
                    document += '<img src="%s" width=500>\n' % filename
            else:
                child.evaluate()

    if len(active_paragraph) > 0:
        document += latex_string_to_html(active_paragraph)
        active_paragraph = ""

    document += ('</div>\n'
                 '</body>\n'
                 '</html>')

    with open("simple.html", 'w') as f:
        f.write(document.encode('utf8'))


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
