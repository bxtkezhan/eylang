from .dragonlexer import reserved
from .dragonlexer import rules as lex_rules
from rply import ParserGenerator

pg = ParserGenerator(
    list(reserved.values()) + [name for name, _ in lex_rules],
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)

@pg.production('program : program statement')
@pg.production('program : statement')
def p_program(p):
    if len(p) == 1:
        line, stat = p[0]
        return {line: stat}
    elif len(p) == 2:
        line, stat = p[1]
        p[0][line] = stat
        return p[0]

@pg.production('statement : command NEWLINE')
def p_statement(p):
    lineno, stat = p[0]
    return (lineno, stat)

@pg.production('statement : NEWLINE')
def p_statement_newline(p):
    # maybe to add box or token
    return (p[0].getsourcepos().lineno, ('NEWLINE', None))

@pg.production('command : NUMBER')
def expression_number(p):
    return (p[0].getsourcepos().lineno, ('NUMBER', p[0].getstr()))

parser = pg.build()
