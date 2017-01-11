#from pylama import latex, markdown
#import markdown
from code import InteractiveConsole

#context = None

class Context(object):

    document = ""
    variables = {}
    global_variables = {}
    context = None

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
            line = lines[nbr]
            woindent = line.lstrip()
            lineindent = len(line) - len(woindent)
            if lineindent == childindent:
                if woindent[0] == '>':
                    self.children.append(Context(self, func=woindent[1:], indent=lineindent))
                    #child_lines = [i for i in range(nbr+1, len(lines)) if compute_indent(lines[i]) > childindent]
                    upper_nbr = nbr+1
                    while upper_nbr < len(lines) and self.compute_indent(lines[upper_nbr]) > childindent:
                        upper_nbr = upper_nbr+1
                    self.children[-1].parse_buf(lines[nbr+1:upper_nbr])
                    nbr = upper_nbr
                else:
                    if len(self.children) == 0 or self.children[-1].function is not None:
                        self.children.append(Context(self, text="", indent=lineindent))
                    print self.children[-1].indent
                    self.children[-1].text += woindent
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
            #console.runcode(self.function)
            Context.variables["__context__"] = self
            Context.variables["__parent__"] = self.parent
            Context.variables["__children__"] = self.children
            #Context.variables["Context"] = Context
            exec "Context.context = __context__" in Context.variables #, Context.global_variables
            exec "Context.parent = __parent__" in Context.variables
            exec "Context.children = __children__" in Context.variables
            exec self.function in Context.variables #, Context.global_variables

            #exec "__context__ = Context.context" in Context.variables
            #Context.variables = Context.variables["Context"].variables

            #exec "__context__ = Context.context" in Context.variables #, Context.global_variables
            #exec "__parent__ = Context.parent" in Context.variables
            #exec "__children__ = Context.children" in Context.variables

            #temp = Context.variables["__context__"]
            #if hasattr(temp, "cell"):
            #    self.cell = temp.cell
            #self.parent = Context.variables["__parent__"]
            #self.children = Context.variables["__children__"]

    def evaluate_children(self):
        for child in self.children:
            child.evaluate()

    def set_global_context(self):
        #global context
        #context = self

        #console.runcode("global context")
        #console.runcode("global parent")
        #console.runcode("global children")
        #console.locals["__context__"] = self
        #console.locals["__parent__"] = self.parent
        #console.locals["__children__"] = self.children
        #onsole.runcode("context = __context__")
        #console.runcode("parent = __parent__")
        #console.runcode("children = __children__")
        #exec "global context\n" in Context.variables
        #Context.variables['context'] = self
        #Context.variables['parent'] = self.parent
        #Context.variables['children'] = self.children
        pass

    #def get_global_context(self):

    def evaluate(self):
        #global context, parent, children
        #context = self
        #parent = self.parent
        #children = self.children
        #console.locals['context'] = self
        #console.locals['parent'] = self.parent
        #console.locals['children'] = self.children

        #self.set_global_context()
        if self.parent is not None and self.function is None:
            #context = console.locals['context']
            Context.document += self.text
            #console.locals['context'] = context
        else:
            #context = console.locals['context']
            self.evaluate_top()
            #for child in self.children:
            #    child.evaluate()
