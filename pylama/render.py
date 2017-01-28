import subprocess
from pylama.context import Context
from pylama.bookkeeping import BookKeeping

def render_standalone(document, imports):

    standalone_document = "\documentclass[preview]{standalone}\n"
    for imp in imports:
        standalone_document += imp + "\n"
    standalone_document += "\\begin{document}\n"
    for block, number in BookKeeping.blocks.items():
        standalone_document += "\\addtocounter{%s}{%d}" % (block, number)
    standalone_document += document
    standalone_document += "\end{document}"

    outfile = "try.tex"

    with open(outfile, 'w') as f:
        f.write(standalone_document)

    pdffile = "try.pdf"
    pngfile = "try.png"
    subprocess.call(['pdflatex', '-shell-escape', outfile, pdffile])
    subprocess.call(['convert', '-density',  '300', '-quality', '90', pdffile, pngfile])

def render():
    document_bkp = Context.document
    Context.document = ""
    for l, (block, number) in BookKeeping.labels.items():
        print "SECTION!"
        if block == 'section':
            print l, number, BookKeeping.blocks['section']
    for l, (block, number) in BookKeeping.labels.items():
        print "SUBSECTION!"
        if block == 'subsection':
            print l, number, BookKeeping.blocks['subsection']
    BookKeeping.is_used = True
    Context.context.add()
    BookKeeping.is_used = False
    if len(Context.document) > 0:
        render_standalone(Context.document, Context.imports)
    Context.document = document_bkp + Context.document
