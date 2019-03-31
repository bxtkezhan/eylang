from .dragonlexer import reserved
from .dragonlexer import rules as lex_rules
from rply import ParserGenerator


pg = ParserGenerator(
    list(reserved.values()) + [name for name, _ in lex_rules],
    precedence=[
        ('left', ['COMMA']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV', 'MOD']),
        ('left', ['POWER']),
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
    return (p[1].getsourcepos().lineno, p[0])

@pg.production('statement : NEWLINE')
def p_statement_newline(p):
    return (p[0].getsourcepos().lineno, (p[0].gettokentype(), None))

@pg.production('command : variable ASSIGN expr')
def p_command_assign(p):
    return ('ASSIGN', (p[0], p[2]))

@pg.production('command : expr')
def p_command_expr(p):
    return ('EXPR', p[0])

@pg.production('expr : rlist RSQB')
def p_expr_list(p):
    return p[0]

@pg.production('rlist : rlist COMMA expr')
@pg.production('rlist : llist expr')
def p_rlist(p):
    if len(p) > 2:
        _, items = p[0]
        items.append(p[2])
    else:
        _, items = p[0]
        items.append(p[1])
    return ('LIST', items)

@pg.production('llist : LSQB expr COMMA')
def p_llist(p):
    return ('LIST', [p[1]])

@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
@pg.production('expr : expr MOD expr')
@pg.production('expr : expr POWER expr')
def p_expr_binary(p):
    return (p[1].gettokentype(), (p[0], p[2]))

@pg.production('expr : LPAR expr RPAR')
def p_expr_parens(p):
    return ('PARENS', p[1])

@pg.production('expr : NUMBER')
@pg.production('expr : STRING')
def p_expr_constant(p):
    return (p[0].gettokentype(), eval(p[0].getstr()))

@pg.production('expr : variable')
def p_expr_variable(p):
    return p[0]

@pg.production('variable : NAME')
def p_variable(p):
    return ('VARIABLE', p[0].getstr())

parser = pg.build()
