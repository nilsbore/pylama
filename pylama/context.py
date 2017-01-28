#import code

import ast
import re

class Context(object):

    document = ""
    variables = {}
    context = None
    parent = None
    children = None
    imports = []

    def __init__(self, myparent, func=None, text=None, indent=0, inline=False):
        self.parent = myparent
        self.children = []
        self.function = func
        self.text = text
        self.indent = indent
        self.inline = inline

        # Is this really needed every time we instantiate a new Context?
        # Doesn't seem like it...
        # exec "from pylama.context import Context" in Context.variables

    def compute_indent(self, line):
        return len(line) - len(line.lstrip())

    def get_function_body(self, line, indent):
        woindent = line.lstrip()
        if len(line)-len(woindent) != indent:
            return ""
        if len(woindent) == 0 or woindent[0] != '>':
            return ""
        return woindent[1:]

    def parse_buf(self, lines):
        if self.function is None:
            childindent = 0
        else:
            childindent = self.indent + 4

        #identifier = re.compile(r"[>][^\d\W]\w*[(].*?[)]") #, re.UNICODE)
        identifier = re.compile(r"[>][^\d\W]\w*[(](?:\"[^\"]+\"|.*?)[)]")

        nbr = 0
        nbr_breaks = 0
        while nbr < len(lines):
            line = lines[nbr]
            woindent = line.lstrip()
            lineindent = len(line) - len(woindent)
            if lineindent == childindent:
                if woindent[0] == '>':
                    nbr_breaks = 0
                    self.children.append(Context(self, func=woindent[1:], indent=lineindent))

                    while nbr+1 < len(lines):
                        body = self.get_function_body(lines[nbr+1], childindent)
                        if len(body) == 0:
                            break
                        self.children[-1].function += body
                        nbr += 1

                    upper_nbr = nbr+1
                    while upper_nbr < len(lines) and self.compute_indent(lines[upper_nbr]) > childindent:
                        upper_nbr = upper_nbr+1
                    self.children[-1].parse_buf(lines[nbr+1:upper_nbr])
                    nbr = upper_nbr
                else:
                    if len(self.children) == 0 or self.children[-1].function is not None:
                        nbr_breaks = 0
                        self.children.append(Context(self, text="", indent=lineindent))
                    self.children[-1].text += "\n"*nbr_breaks

                    # this code checks for inline python code
                    matches = identifier.finditer(woindent)
                    splits = identifier.split(woindent)
                    for te, fn in zip(splits, matches):
                        self.children[-1].text += te
                        self.children.append(Context(self, func=fn.group()[1:], indent=lineindent, inline=True))
                        self.children.append(Context(self, text="", indent=lineindent))

                    if len(splits[-1]) == 0: # this should never happen
                        self.children.pop()
                    else:
                        self.children[-1].text += splits[-1] #woindent
                    nbr = nbr + 1
                    nbr_breaks = 0
            elif len(woindent) == 0:
                if len(self.children) > 0 and self.children[-1].function is None:
                    nbr_breaks += 1
                nbr = nbr + 1
            else:
                nbr_breaks = 0
                nbr = nbr + 1
                print "This all went to hell, returning..."

    def print_parse_tree(self, indent=0):
        indent_str = " "*indent
        function_str = " "*len("Function: ")
        text_str = " "*len("Text: ")
        parent_str = " "*len("Parent: ")
        print indent_str + "==================="
        print indent_str + "Function: " + str(self.function).rstrip().replace("\n", "\n"+indent_str+function_str)
        print indent_str + "Text: " + str(self.text).rstrip().replace("\n", "\n"+indent_str+text_str)
        print indent_str + "Indent: " + str(self.indent)
        if self.parent is None:
            print indent_str + "No Parent!"
        else:
            print indent_str + "Parent: " + str(self.parent.function).rstrip().replace("\n", "\n"+indent_str+parent_str)
        print indent_str + "==================="
        for nbr, child in enumerate(self.children):
            child.print_parse_tree(indent+4)

    def evaluate_top(self):
        if self.function is not None:
            context_bkp = Context.context
            parent_bkp = Context.parent
            children_bkp = Context.children

            Context.context = self
            Context.parent = self.parent
            Context.children = self.children

            keywords = {}
            restore = {}
            last_row = self.function.splitlines()[-1].lstrip()
            call = ast.parse(last_row)
            if len(call.body) > 0 and \
              (isinstance(call.body[0], ast.Expr) or isinstance(call.body[0], ast.Assign)) and \
               isinstance(call.body[0].value, ast.Call):
                for kw in call.body[0].value.keywords:
                    if kw.arg in Context.variables:
                        restore[kw.arg] = Context.variables[kw.arg]
                    value = None
                    # this is all a bit too much now that we can compile stuff
                    if isinstance(kw.value, ast.Name):
                        if kw.value.id in Context.variables:
                            value = Context.variables[kw.value.id]
                        else:
                            value = None
                    elif isinstance(kw.value, ast.Expr) or isinstance(kw.value, ast.Call):
                        expr = ast.Expression(kw.value)
                        value = eval(compile(expr, '', 'eval'), Context.variables)
                    else:
                        value = ast.literal_eval(kw.value)
                    if value is not None:
                        keywords[kw.arg] = value
                        Context.variables[kw.arg] = value

            Context.variables["Context"] = Context

            exec self.function in Context.variables

            for k,v in keywords.items():
                Context.variables.pop(k)

            for k,v in restore.items():
                Context.variables[k] = v

            Context.context = context_bkp
            Context.parent = parent_bkp
            Context.children = children_bkp
        else:
            print "Self.function is none!"

    def add(self):
        for child in self.children:
            child.evaluate()

    def evaluate(self):

        if self.parent is not None and self.function is None:
            Context.document += self.text
        else:
            self.evaluate_top()
