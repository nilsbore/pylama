from pylama import latex

latex("\usepackage{graphicx}")

def figure(image, caption=None, label=None, placement="t", width="\textwidth", scale=1.0, context):
    latex("\begin{figure*}[%s]" % (placement))

    context.evaluate()

    latex("\begin{subfigure}[%s]{%s} \
		   \center \
		   \includegraphics[scale=%f]{%s} \
	       \end{subfigure}" % (placement, width, scale, image))

    if not caption is None:
        latex("\caption{%s}" % caption)
    if not label is None:
        latex("\label{%s}" % label)
    latex("\end{figure*}")
