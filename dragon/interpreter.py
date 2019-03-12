from rply import LexerGenerator
from rply import ParserGenerator

from dragon.value import Value
from dragon import operator

import tokenize


DRAGON_VARS = dict()

lg = LexerGenerator()

lg.add('IMAGE_NUMBER', tokenize.Imagnumber)
lg.add('FLOAT_NUMBER', tokenize.Floatnumber)
lg.add('INT_NUMBER', tokenize.Intnumber)
lg.add('STRING', tokenize.String)
lg.add('NAME', r'[_a-zA-Z][_0-9a-zA-Z]*')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('OPEN_PARENS', r'\(')
lg.add('CLOSE_PARENS', r'\)')
lg.add('EQUAL', r'=')

lg.ignore('\s+')

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['IMAGE_NUMBER', 'FLOAT_NUMBER', 'INT_NUMBER', 'STRING', 'NAME',
     'EQUAL', 'OPEN_PARENS', 'CLOSE_PARENS', 'PLUS', 'MINUS', 'MUL', 'DIV'
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['EQUAL']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)

@pg.production('expression : INT_NUMBER')
@pg.production('expression : FLOAT_NUMBER')
@pg.production('expression : IMAGE_NUMBER')
def expression_number(p):
    if p[0].gettokentype() == 'INT_NUMBER':
        return Value(int(p[0].getstr()))
    elif p[0].gettokentype() == 'FLOAT_NUMBER':
        return Value(float(p[0].getstr()))
    elif p[0].gettokentype() == 'IMAGE_NUMBER':
        return Value(complex(p[0].getstr()))

@pg.production('expression : STRING')
def expression_string(p):
    return Value(eval(p[0].getstr()))

@pg.production('expression : NAME')
def expression_variable(p):
    name = p[0].getstr()
    if name in DRAGON_VARS:
        return Value(DRAGON_VARS[name])
    else:
        raise NameError("name '{}' is not defined".format(name))

@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(p):
    return p[1]

@pg.production('expression : PLUS expression')
@pg.production('expression : MINUS expression')
def expression_oneop(p):
    if p[0].gettokentype() == 'PLUS':
        return operator.Positive(p[1])
    elif p[0].gettokentype() == 'MINUS':
        return operator.Negative(p[1])
    else:
        raise AssertionError('Oops, this should not be possible!')

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(p):
    if p[1].gettokentype() == 'PLUS':
        return operator.Add(p[0], p[2])
    elif p[1].gettokentype() == 'MINUS':
        return operator.Sub(p[0], p[2])
    elif p[1].gettokentype() == 'MUL':
        return operator.Mul(p[0], p[2])
    elif p[1].gettokentype() == 'DIV':
        return operator.Div(p[0], p[2])
    else:
        raise AssertionError('Oops, this should not be possible!')

@pg.production('expression : NAME EQUAL expression')
def expression_assignment(p):
    name = p[0].getstr()
    data = p[2].eval()
    DRAGON_VARS[name] = data
    return Value(data)

@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())

lexer = lg.build()
parser = pg.build()
