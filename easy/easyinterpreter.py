from rply.token import BaseBox
from rply.token import Token


class Constant(BaseBox):
    def __init__(self, value):
        self.value = eval(value.getstr())

    def eval(self):
        return self.value

    def __repr__(self):
        return '{!r}'.format(self.value)

class Variable(BaseBox):
    def __init__(self, name, var_dict):
        self.name = name.getstr()
        self.var_dict = var_dict

    def set(self, value):
        self.var_dict[self.name] = value

    def eval(self):
        return self.var_dict[self.name]

    def __repr__(self):
        return '{}'.format(self.name)

class Attribute(BaseBox):
    def __init__(self, obj, attr, var_dict):
        self.obj = obj
        self.attr = attr
        self.var_dict = var_dict

    def set(self, value):
        setattr(self.obj.eval(), self.attr.name, value)

    def eval(self):
        return getattr(self.obj.eval(), self.attr.name)

    def __repr__(self):
        return '{}.{}'.format(self.obj, self.attr)

class VarList(BaseBox):
    def __init__(self, varlist=[]):
        self.varlist = varlist

    def append(self, var):
        self.varlist.append(var)

    def eval(self):
        return self.varlist

    def __repr__(self):
        return ', '.join(map(str, self.varlist))

class Index(BaseBox):
    def __init__(self, expr, indexlist):
        self.expr = expr
        self.indexlist = indexlist

    def parseindex(self, index):
        if len(index) == 1:
                return index[0].eval()
        else:
            return slice(*((item.eval() if item else None) for item in index))

    def eval(self):
        if len(self.indexlist) == 1:
            return self.expr.eval()[self.parseindex(self.indexlist[0])]
        return self.expr.eval()[[self.parseindex(index) for index in self.indexlist]]

    def index2str(self, index):
        if len(index) == 1:
                return repr(index[0])
        else:
            return 'slice({})'.format(','.join(repr(item) for item in index))

    def __repr__(self):
        if len(self.indexlist) == 1:
            return '({!r}[{}])'.format(self.expr, self.index2str(self.indexlist[0]))
        return '({!r}[{}])'.format(self.expr, ', '.join(self.index2str(index) for index in self.indexlist))

class List(BaseBox):
    def __init__(self, exprlist=[]):
        self.exprlist = exprlist

    def eval(self):
        return [expr.eval() for expr in self.exprlist]

    def __repr__(self):
        return '{!r}'.format(self.exprlist)

class Dictionary(BaseBox):
    def __init__(self, pairlist={}):
        self.pairlist = pairlist

    def set(self, key, value):
        self.pairlist[key.eval()] = value.eval()

    def get(self, key):
        return self.pairlist[key.eval()]

    def eval(self):
        return {key.eval(): value.eval() for key, value in self.pairlist.items()}

    def __repr__(self):
        return '{!r}'.format(self.pairlist)

class Func(BaseBox):
    def __init__(self, obj, arglist=None):
        self.obj = obj
        self.arglist = arglist

    def eval(self):
        try:
            if self.arglist is None:
                result = self.obj.eval()()
            else:
                result = self.obj.eval()(self.arglist.eval())
        except ReturnInterrupt as e:
            result = e.result
        return result

    def __repr__(self):
        if self.arglist is not None:
            return '{!r}({!r})'.format(self.obj, self.arglist)
        else:
            return '{!r}()'.format(self.obj)

class Parens(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        return self.expr.eval()

    def __repr__(self):
        return '({!r})'.format(self.expr)

class Sign(BaseBox):
    def __init__(self, opt, expr):
        self.opt = opt.getstr()
        self.expr = expr

    def eval(self):
        if self.opt == '+':
            return + self.expr.eval()
        elif self.opt == '-':
            return - self.expr.eval()

    def __repr__(self):
        return '{}{!r}'.format(self.opt, self.expr)

class BinaryOp(BaseBox):
    def __init__(self, opt, left, right):
        self.opt = opt.getstr()
        self.left = left
        self.right = right

    def eval(self):
        if self.opt == '+':
            return self.left.eval() + self.right.eval()
        elif self.opt == '-':
            return self.left.eval() - self.right.eval()
        elif self.opt == '*':
            return self.left.eval() * self.right.eval()
        elif self.opt == '/':
            return self.left.eval() / self.right.eval()
        elif self.opt == '%':
            return self.left.eval() % self.right.eval()
        elif self.opt == '^':
            return self.left.eval() ** self.right.eval()
        elif self.opt == '==':
            return self.left.eval() == self.right.eval()
        elif self.opt == '<':
            return self.left.eval() < self.right.eval()
        elif self.opt == '<=':
            return self.left.eval() <= self.right.eval()
        elif self.opt == '>':
            return self.left.eval() > self.right.eval()
        elif self.opt == '>=':
            return self.left.eval() >= self.right.eval()
        elif self.opt == '!=':
            return self.left.eval() != self.right.eval()

    def __repr__(self):
        return '{!r} {} {!r}'.format(self.left, self.opt, self.right)

class Expr(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        return self.expr.eval()

    def __repr__(self):
        return '{!r}'.format(self.expr)

class Assign(BaseBox):
    def __init__(self, varlist, expr):
        self.varlist = varlist
        self.expr = expr

    def eval(self):
        varlist = self.varlist.eval()
        if len(varlist) == 1:
            varlist[0].set(self.expr.eval())
        else:
            values = self.expr.eval()
            for i, value in enumerate(values):
                varlist[i].set(value)

    def __repr__(self):
        return '{} = {!r}'.format(self.varlist, self.expr)

class Puts(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        print(self.expr.eval())

    def __repr__(self):
        return 'puts {!r}'.format(self.expr)

class ELIF(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        return self.expr.eval()

    def __repr__(self):
        return 'elif {!r} then'.format(self.expr)

class IF(BaseBox):
    def __init__(self, expr, program1, program2=None):
        self.expr = expr
        self.program1 = program1
        self.program2 = program2

    def eval(self):
        statements = self.program1.statements
        lines = sorted(statements.keys())
        if self.expr.eval():
            for line in lines:
                command = statements[line]
                if isinstance(command, ELIF): break
                command.eval()
        else:
            elif_content_start = len(lines)
            for i, line in enumerate(lines):
                command = statements[line]
                if isinstance(command, ELIF) and command.eval():
                    elif_content_start = i + 1
                    break
            if elif_content_start < len(lines):
                for line in lines[elif_content_start:]:
                    command = statements[line]
                    if isinstance(command, ELIF): break
                    command.eval()
            elif self.program2 is not None:
                self.program2.eval()

    def __repr__(self):
        if self.program2 is None:
            return 'if {!r} then\n{!r}\nend'.format(self.expr, self.program1)
        else:
            return 'if {!r} then\n{!r}\nelse\n{!r}\nend'.format(self.expr, self.program1, self.program2)

class While(BaseBox):
    def __init__(self, expr, program1, program2=None):
        self.expr = expr
        self.program1 = program1
        self.program2 = program2

    def eval(self):
        while self.expr.eval():
            self.program1.eval()
        else:
            if self.program2 is not None:
                self.program2.eval()

    def __repr__(self):
        if self.program2 is None:
            return 'while {!r} then\n{!r}\nend'.format(self.expr, self.program1)
        else:
            return 'while {!r} then\n{!r}\nelse\n{!r}\nend'.format(self.expr, self.program1, self.program2)

class For(BaseBox):
    def __init__(self, varlist, expr, program1, program2=None):
        self.varlist = varlist
        self.expr = expr
        self.program1 = program1
        self.program2 = program2

    def eval(self):
        varlist = self.varlist.eval()
        for values in self.expr.eval():
            if len(varlist) == 1:
                varlist[0].set(values)
            else:
                for variable, value in zip(varlist, values):
                    variable.set(value)
            self.program1.eval()
        else:
            if self.program2 is not None:
                self.program2.eval()

    def __repr__(self):
        if self.program2 is None:
            return 'for {!r} in {!r} then\n{!r}\nend'.format(self.varlist, self.expr, self.program1)
        else:
            return 'for {!r} in {!r} then\n{!r}\nelse\n{!r}\nend'.format(self.varlist, self.expr, self.program1, self.program2)

class EasyFunc:
    def __init__(self, paralist, program):
        self.paralist = paralist
        self.program = program

    def __call__(self, args=None):
        self.paralist.eval()
        if args is not None:
            args, kwargs = args
            for i, value in enumerate(args):
                self.paralist.set(i, value)
            for variable, value in kwargs:
                variable.set(value)
        self.program.eval()

class ParaList:
    def __init__(self, item=None):
        self.items = [] if item is None else [item]

    def append(self, item):
        self.items.append(item)

    def set(self, index, value):
        self.items[index][0].set(value)

    def eval(self):
        for item in self.items:
            if len(item) == 1:
                item[0].set(None)
            else:
                item[0].set(item[1].eval())

    def __repr__(self):
        args = ', '.join(repr(item[0]) for item in self.items if len(item) == 1)
        kwargs = ', '.join('{!r}={!r}'.format(item[0], item[1]) for item in self.items if len(item) == 2)
        return args + ', ' * bool(args) * bool(kwargs) + kwargs

class ArgList:
    def __init__(self, item=None):
        self.items = [] if item is None else [item]

    def append(self, item):
        self.items.append(item)

    def eval(self):
        args = []
        kwargs = []
        for item in self.items:
            if len(item) == 1:
                args.append(item[0].eval())
            else:
                kwargs.append((item[0], item[1].eval()))
        return args, kwargs

    def __repr__(self):
        args = ', '.join(repr(item[0]) for item in self.items if len(item) == 1)
        kwargs = ', '.join('{!r}={!r}'.format(item[0], item[1]) for item in self.items if len(item) == 2)
        return args + ', ' * bool(args) * bool(kwargs) + kwargs

class DEF(BaseBox):
    def __init__(self, variable, program, paralist=None):
        self.variable = variable
        self.paralist = paralist
        self.program = program

    def eval(self):
        self.variable.set(EasyFunc(self.paralist, self.program))

    def __repr__(self):
        if self.paralist is None:
            return 'def {!r}() then\n{!r}\nend'.format(self.variable, self.program)
        else:
            return 'def {!r}({!r}) then\n{!r}\nend'.format(self.variable, self.paralist, self.program)

class ReturnInterrupt(Exception):
    def __init__(self, result):
        super().__init__(result)
        self.result = result

class Return(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        raise ReturnInterrupt(self.expr.eval())

    def __repr__(self):
        return 'return {!r}'.format(self.expr)

class Newline(BaseBox):
    def eval(self):
        return None

    def __repr__(self):
        return 'NEWLINE'

class Program(BaseBox):
    def __init__(self, statements={}):
        self.statements = statements

    def set(self, line, stat):
        self.statements[line] = stat

    def eval(self):
        lines = sorted(self.statements.keys())
        for line in lines[:-1]:
            self.statements[line].eval()
        return self.statements[lines[-1]].eval()

    def __repr__(self):
        return '\n'.join('{}. {!r}'.format(line, self.statements[line])
                for line in sorted(self.statements.keys()))
