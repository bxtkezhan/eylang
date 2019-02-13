from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
import cmd


DRAGON_GLOBALS = dict()

class Number(BaseBox):
    def __init__(self, value):
        self.value = value

    def getvalue(self):
        return self.value

    def __repr__(self):
        return str(self.getvalue())

lg = LexerGenerator()

lg.add('WORD', r'[_a-zA-Z\u2e80-\u9fff]+[_a-zA-Z0-9\u2e80-\u9fff]*')
lg.add('EQUAL', r'=')
lg.add('NUMBER', r'\d+\.?\d*')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('TIMES', r'\*')
lg.add('DIVIDE', r'/')
lg.add('OPEN_PARENS', r'\(')
lg.add('CLOSE_PARENS', r'\)')

lg.ignore(r'\s+')

pg = ParserGenerator(
        ['WORD', 'EQUAL', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'OPEN_PARENS', 'CLOSE_PARENS'],
        precedence=[
            ('left', ['EQUAL']),
            ('left', ['PLUS', 'MINUS']),
            ('left', ['TIMES', 'DIVIDE'])])

@pg.production('expression : WORD')
def expression_word(p):
    var_name = p[0].getstr()
    if var_name in DRAGON_GLOBALS:
        return Number(DRAGON_GLOBALS[var_name])
    print("NameError: name '{}' is not defined".format(var_name))

@pg.production('expression : WORD EQUAL expression')
def expression_assignment(p):
    DRAGON_GLOBALS[p[0].getstr()] = p[2].getvalue()

@pg.production('expression : NUMBER')
def expression_number(p):
    return Number(float(p[0].getstr()))

@pg.production('expression : PLUS expression')
def expression_positive(p):
    return Number(p[1].getvalue())

@pg.production('expression : MINUS expression')
def expression_negative(p):
    return Number(-p[1].getvalue())

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
        return Number(lhs + rhs)
    elif p[1].gettokentype() == 'MINUS':
        return Number(lhs - rhs)
    elif p[1].gettokentype() == 'TIMES':
        return Number(lhs * rhs)
    elif p[1].gettokentype() == 'DIVIDE':
        return Number(lhs / rhs)
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
        if result: print(result)


if __name__ == '__main__':
    print('Dragon Programming Language DEV.')
    shell = Shell()
    while True:
        try:
            shell.cmdloop()
            break
        except KeyboardInterrupt as e:
            print()
