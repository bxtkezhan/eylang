from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from collections import OrderedDict
import cmd
import tokenize
from string import Template


DRAGON_VAR = OrderedDict()

class Variable(BaseBox):
    def __init__(self, value):
        self.value = value

    def getvalue(self):
        return self.value

    def __repr__(self):
        if isinstance(self.value, float):
            return '{:g}'.format(self.value)
        return str(self.value)

lg = LexerGenerator()

lg.add('WORD', r'[_a-zA-Z][_a-zA-Z0-9]*')
lg.add('MAGIC_KEY', r'^[ \\f\\t ]*\$[_a-zA-Z][_a-zA-Z0-9]*')
lg.add('NUMBER', tokenize.Number)
lg.add('STRING', tokenize.String)
lg.add('EQUAL', r'=')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('TIMES', r'\*')
lg.add('DIVIDE', r'/')
lg.add('OPEN_PARENS', r'\(')
lg.add('CLOSE_PARENS', r'\)')

lg.ignore(r'\s+')

pg = ParserGenerator(
        ['WORD', 'MAGIC_KEY', 'NUMBER', 'STRING',
         'EQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'OPEN_PARENS', 'CLOSE_PARENS'],
        precedence=[
            ('left', ['EQUAL']),
            ('left', ['PLUS', 'MINUS']),
            ('left', ['TIMES', 'DIVIDE'])])

@pg.production('expression : WORD')
def expression_word(p):
    var_name = p[0].getstr()
    if var_name in DRAGON_VAR:
        return Variable(DRAGON_VAR[var_name])
    print("NameError: name '{}' is not defined".format(var_name))

@pg.production('expression : NUMBER')
def expression_number(p):
    number = float(p[0].getstr())
    if number.is_integer():
        return Variable(int(number))
    return Variable(number)

@pg.production('expression : STRING')
def expression_string(p):
    template = Template(eval(p[0].getstr()))
    return Variable(template.substitute(DRAGON_VAR))

@pg.production('expression : MAGIC_KEY')
def expression_magic_key(p):
    key = p[0].getstr()[1:]
    if key == 'var':
        print(dict(DRAGON_VAR))
    elif key == 'out':
        print(DRAGON_VAR.get('$out', ''))

@pg.production('expression : WORD EQUAL expression')
def expression_assignment(p):
    DRAGON_VAR[p[0].getstr()] = p[2].getvalue()

@pg.production('expression : PLUS expression')
def expression_positive(p):
    return Variable(p[1].getvalue())

@pg.production('expression : MINUS expression')
def expression_negative(p):
    return Variable(-p[1].getvalue())

@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(p):
    return p[1]

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression TIMES expression')
@pg.production('expression : expression DIVIDE expression')
def expression_operator(p):
    lhs = p[0].getvalue()
    rhs = p[2].getvalue()
    if p[1].gettokentype() == 'PLUS':
        return Variable(lhs + rhs)
    elif p[1].gettokentype() == 'MINUS':
        return Variable(lhs - rhs)
    elif p[1].gettokentype() == 'TIMES':
        return Variable(lhs * rhs)
    elif p[1].gettokentype() == 'DIVIDE':
        return Variable(lhs / rhs)
    else:
        raise AssertionError('This is impossible, abort the time machine!')


class Shell(cmd.Cmd):
    prompt = 'dragon> '

    def __init__(self):
        super(Shell, self).__init__()
        self.lexer = lg.build()
        self.parser = pg.build()

    def do_EOF(self, args):
        print('bye!')
        return True
    do_bye = do_EOF
    do_quit = do_EOF

    def default(self, line):
        result = self.parser.parse(self.lexer.lex(line))
        if result is not None:
            DRAGON_VAR['$out'] = result.getvalue()
            print(result)


if __name__ == '__main__':
    print('Dragon Programming Language DEV.')
    shell = Shell()
    while True:
        try:
            shell.cmdloop()
            break
        except KeyboardInterrupt as e:
            print()
