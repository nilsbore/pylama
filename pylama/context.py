
class Context(object):

    document = ""
    variables = {}
    context = None
    parent = None
    children = None

    def __init__(self, parent, func=None, text=None, indent=0):
        self.parent = parent
        self.children = []
        self.function = func
        self.text = text
        self.indent = indent
        exec "from pylama.context import Context" in Context.variables

    def compute_indent(self, line):
        return len(line) - len(line.lstrip())

    def parse_buf(self, lines):
        if self.function is None:
            childindent = 0
        else:
            childindent = self.indent + 4

        nbr = 0
        while nbr < len(lines):
            #print lines[nbr]
            line = lines[nbr]
            woindent = line.lstrip()
            lineindent = len(line) - len(woindent)
            if lineindent == childindent:
                if woindent[0] == '>':
                    self.children.append(Context(self, func=woindent[1:], indent=lineindent))
                    upper_nbr = nbr+1
                    while upper_nbr < len(lines) and self.compute_indent(lines[upper_nbr]) > childindent:
                        upper_nbr = upper_nbr+1
                    self.children[-1].parse_buf(lines[nbr+1:upper_nbr])
                    nbr = upper_nbr
                else:
                    if len(self.children) == 0 or self.children[-1].function is not None:
                        self.children.append(Context(self, text="", indent=lineindent))
                    self.children[-1].text += woindent
                    nbr = nbr + 1
            elif len(woindent) == 0:
                if len(self.children) > 0 and self.children[-1].function is None:
                    pass#self.children[-1].text += "\n"
                nbr = nbr + 1
            else:
                nbr = nbr + 1
                print "This all went to hell, returning..."

    def print_parse_tree(self, indent=0):
        indent_str = " "*indent
        print indent_str + "==================="
        print indent_str + "Function: " + str(self.function)
        print indent_str + "Text: " + str(self.text)
        print indent_str + "Indent: " + str(self.indent)
        print indent_str + "==================="
        for nbr, child in enumerate(self.children):
            child.print_parse_tree(indent+4)

    def evaluate_top(self):
        if self.function is not None:
            #Context.variables["__context__"] = self
            #Context.variables["__parent__"] = self.parent
            #Context.variables["__children__"] = self.children
            #exec "Context.context = __context__" in Context.variables #, Context.global_variables
            #exec "Context.parent = __parent__" in Context.variables
            #exec "Context.children = __children__" in Context.variables
            Context.context = self
            Context.parent = self.parent
            Context.children = self.children
            Context.variables["Context"] = Context
            exec self.function in Context.variables

            #exec "__context__ = Context.context" in Context.variables
            #Context.variables = Context.variables["Context"].variables

            #exec "__context__ = Context.context" in Context.variables #, Context.global_variables
            #exec "__parent__ = Context.parent" in Context.variables
            #exec "__children__ = Context.children" in Context.variables

            #temp = Context.variables["__context__"]
            #self.parent = Context.variables["__parent__"]
            #self.children = Context.variables["__children__"]

    def add(self):
        for child in self.children:
            child.evaluate()

    def evaluate(self):

        if self.parent is not None and self.function is None:
            Context.document += self.text
        else:
            self.evaluate_top()
