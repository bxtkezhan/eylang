from rply.token import BaseBox


class Constant(BaseBox):
    def __init__(self, value):
        self.value = eval(value.getstr())

    def eval(self):
        return self.value

    def __repr__(self):
        return '{!r}'.format(self.value)

    def __str__(self):
        return '{}'.format(self.value)

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

    def __str__(self):
        return '{}'.format(self.name)

class VarList(BaseBox):
    def __init__(self, varlist=[]):
        self.varlist = varlist

    def append(self, var):
        self.varlist.append(var)

    def eval(self):
        return self.varlist

    def __repr__(self):
        return ', '.join(map(str, self.varlist))

    def __str__(self):
        return ', '.join(map(str, self.varlist))

class Parens(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        return self.expr.eval()

    def __repr__(self):
        return '({!r})'.format(self.expr)

    def __str__(self):
        return '{}'.format(self.expr)

class BinOp(BaseBox):
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

    def __str__(self):
        return '{} {} {}'.format(self.left, self.opt, self.right)

class Expr(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        return self.expr.eval()

    def __repr__(self):
        return '(EXPR: {!r})'.format(self.expr)

    def __str__(self):
        return '{}'.format(self.expr)

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
        return '(ASSIGN: {} = {!r})'.format(self.varlist, self.expr)

    def __str__(self):
        return '{} = {}'.format(self.varlist, self.expr)

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
        return '\n'.join('{}: {!r}'.format(line, self.statements[line])
                for line in sorted(self.statements.keys()))

    def __str__(self):
        return '{}'.format(self.statements)
