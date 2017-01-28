from pylama.convenience import latex, latex_import

latex_import("\usepackage{hyperref}")

def url(url_string):
    latex("\url{%s}" % url_string)
