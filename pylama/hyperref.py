from pylama.common import latex

latex("\usepackage{hyperref}")

def url(url_string):
    latex("\url{%s}" % url_string)
