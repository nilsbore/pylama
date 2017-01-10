from pylama import latex, markdown
#import markdown
from code import InteractiveConsole

context = None

class Context(object):

    document = ""

    def __init__(self, parent, func=None, text=None, indent=0):
        self.parent = parent
        self.children = []
        self.function = func
        self.text = text
        self.indent = indent

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

    def evaluate_top(self, console):
        if self.function is not None:
            console.runcode(self.function)

    def set_global_context(self, console):
        global context
        context = self

        console.runcode("global context")
        console.runcode("global parent")
        console.runcode("global children")
        console.locals["__context__"] = self
        console.locals["__parent__"] = self.parent
        console.locals["__children__"] = self.children
        console.runcode("context = __context__")
        console.runcode("parent = __parent__")
        console.runcode("children = __children__")

    #def get_global_context(self):

    def evaluate(self, console):
        #global context, parent, children
        #context = self
        #parent = self.parent
        #children = self.children
        #console.locals['context'] = self
        #console.locals['parent'] = self.parent
        #console.locals['children'] = self.children
        self.set_global_context(console)
        if self.parent is not None and self.function is None:
            #context = console.locals['context']
            print "Text context:"
            print self.indent
            print self.function
            print self.text
            #document += self.text
            #console.locals['context'] = context
        else:
            #context = console.locals['context']
            print "Code context:"
            print self.indent
            print self.function
            print self.text
            self.evaluate_top(console)
            for child in self.children:
                child.evaluate(console)
