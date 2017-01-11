from pylama.convenience import latex, maybe_caption, randomref
from pylama.context import Context

latex("\usepackage{graphicx}")

def figure(image, caption=None, label=None, placement="t", scale=1.0):
    if label is None:
        label = randomref()

    latex("\\begin{figure}[%s]" % (placement))

    Context.context.add()

    latex("\includegraphics[scale=%f]{%s}" % (scale, image))

    if not caption is None:
        latex("\caption{%s}" % caption)

    latex("\label{%s}" % label)
    latex("\end{figure}")

    return label