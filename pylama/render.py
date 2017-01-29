import subprocess
from pylama.context import Context
from pylama.bookkeeping import BookKeeping
from pylama.convenience import randomref
import os
import hashlib

def render_standalone(document, imports, name=None):
    if name is None:
        name=randomref()

    tempdir = ".tmp"

    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    mnew = hashlib.md5(document).hexdigest()
    pngfile = os.path.join(tempdir, "%s.png" % name)
    md5file = os.path.join(tempdir, "%s.md5" % name)
    if os.path.exists(md5file):
        # we also need to check if the ref counters are the same
        with open(md5file) as f:
            mold = f.readline()
        if mnew == mold:
            return pngfile

    with open(md5file, 'w') as f:
        f.write(mnew)

    standalone_document = "\documentclass[preview]{standalone}\n"
    for imp in imports:
        standalone_document += imp + "\n"
    standalone_document += "\\begin{document}\n"
    for block, number in BookKeeping.blocks.items():
        standalone_document += "\\addtocounter{%s}{%d}" % (block, number)
    standalone_document += document
    standalone_document += "\end{document}"

    texfile = os.path.join(tempdir, "%s.tex" % name)

    with open(texfile, 'w') as f:
        f.write(standalone_document)

    pdffile = os.path.join(tempdir, "%s.pdf" % name)
    subprocess.call(['pdflatex', '-output-directory', os.path.abspath(tempdir), '-shell-escape', texfile])
    subprocess.call(['convert', '-density',  '300', '-quality', '90', pdffile, pngfile])

    return pngfile

def render(name=None):
    document_bkp = Context.document
    Context.document = ""
    # for l, (block, number) in BookKeeping.labels.items():
    #     print "SECTION!"
    #     if block == 'section':
    #         print l, number, BookKeeping.blocks['section']
    # for l, (block, number) in BookKeeping.labels.items():
    #     print "SUBSECTION!"
    #     if block == 'subsection':
    #         print l, number, BookKeeping.blocks['subsection']
    BookKeeping.is_used = True
    Context.context.add()
    BookKeeping.is_used = False
    if len(Context.document) > 0:
        image_file = render_standalone(Context.document, Context.imports)
    else:
        image_file = None
    Context.document = document_bkp + Context.document

    return image_file
