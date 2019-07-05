from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
import tokenize
import operator
import readline


global_vars = {}

lg = LexerGenerator()

rules = [
    ['NUMBER', tokenize.Number],
    ['NAME', tokenize.Name],
    ['PLUS', r'\+'],
    ['MINUS', r'-'],
    ['MUL', r'\*'],
    ['POWER', r'\^'],
    ['DIV', r'/'],
    ['MOD', r'%'],
    ['LPAR', r'\('],
    ['RPAR', r'\)'],
    ['ASSIGN', r'=']]

for name, regex in rules:
    lg.add(name, regex)

lg.ignore(r'\s+')

pg = ParserGenerator(
    [name for name, _ in rules],
    precedence=[
        ('left', ['ASSIGN']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV', 'MOD']),
        ('left', ['POWER']),
        ('right', ['SIGN']),
    ]
)

@pg.production('main : expr')
def main(p):
    return p[0]

@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
@pg.production('expr : expr MOD expr')
@pg.production('expr : expr POWER expr')
def expr_op(p):
    ops = {
        'PLUS': operator.add,
        'MINUS': operator.sub,
        'MUL': operator.mul,
        'DIV': operator.truediv,
        'MOD': operator.mod,
        'POWER': operator.pow
    }

    lhs = p[0].getvalue()
    rhs = p[2].getvalue()
    opt = ops.get(p[1].gettokentype())
    if opt: return BoxNumber(opt(lhs, rhs))

    raise AssertionError('This is impossible, abort the time machine!')

@pg.production('expr : PLUS expr', precedence='SIGN')
@pg.production('expr : MINUS expr', precedence='SIGN')
def expr_sign(p):
    num = p[1].getvalue()
    if p[0].gettokentype() == 'PLUS':
        return BoxNumber(num)
    else:
        return BoxNumber(-num)

@pg.production('expr : LPAR expr RPAR')
def expr_pars(p):
    return p[1]

@pg.production('expr : NAME ASSIGN expr')
def expr_assign(p):
    global_vars[p[0].getstr()] = p[2]
    return p[2]

@pg.production('expr : NUMBER')
def expr_num(p):
    return BoxNumber(eval(p[0].getstr()))

@pg.production('expr : NAME')
def expr_name(p):
    return global_vars.get(p[0].getstr(), BoxNumber(0))

lexer = lg.build()
parser = pg.build()

class BoxNumber(BaseBox):
    def __init__(self, value):
        self.value = value

    def getvalue(self):
        return self.value

while True:
    try:
        user_input = input('>> ').strip()
    except EOFError: break

    if user_input:
        result = parser.parse(lexer.lex(user_input))
        print(result.getvalue())
