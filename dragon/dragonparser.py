from .dragonlexer import reserved
from .dragonlexer import rules as lex_rules
from rply import ParserGenerator


pg = ParserGenerator(
    list(reserved.values()) + [name for name, _ in lex_rules],
    precedence=[
        ('left', ['AND', 'OR', 'NOT']),
        ('left', ['EQ', 'LT', 'LE', 'GT', 'GE', 'NE']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV', 'MOD']),
        ('left', ['POWER']),
        ('left', ['UMINUS']),
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

@pg.production('command : RETURN expr')
def p_command_return(p):
    return ('RETURN', p[1])

@pg.production('command : DEF variable LPAR paralist RPAR NEWLINE program END')
@pg.production('command : DEF variable LPAR RPAR NEWLINE program END')
def p_command_def(p):
    if len(p) > 7:
        return ('DEF', (p[1], p[3], p[6]))
    else:
        return ('DEF', (p[1], p[5]))

@pg.production('command : FOR varlist IN expr NEWLINE program ELSE NEWLINE program END')
@pg.production('command : FOR varlist IN expr NEWLINE program END')
def p_command_for(p):
    if len(p) > 7:
        return ('FOR', (p[1], p[3], p[5], p[8]))
    else:
        return ('FOR', (p[1], p[3], p[5]))

@pg.production('command : WHILE expr NEWLINE program ELSE NEWLINE program END')
@pg.production('command : WHILE expr NEWLINE program END')
def p_command_while(p):
    if len(p) > 5:
        return ('WHILE', (p[1], p[3], p[6]))
    else:
        return ('WHILE', (p[1], p[3]))

@pg.production('command : ELIF expr')
def p_command_elif(p):
    return ('ELIF', p[1])

@pg.production('command : IF expr NEWLINE program ELSE NEWLINE program END')
@pg.production('command : IF expr NEWLINE program END')
def p_command_if(p):
    if len(p) > 5:
        return ('IF', (p[1], p[3], p[6]))
    else:
        return ('IF', (p[1], p[3]))

@pg.production('command : varlist ASSIGN expr')
def p_command_assign(p):
    return ('ASSIGN', (p[0], p[2]))

@pg.production('command : PUTS expr')
def p_command_puts(p):
    return ('PUTS', p[1])

@pg.production('command : expr')
def p_command_expr(p):
    return ('EXPR', p[0])

@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
@pg.production('expr : expr MOD expr')
@pg.production('expr : expr POWER expr')
def p_expr_binop(p):
    return (p[1].gettokentype(), (p[0], p[2]))

@pg.production('expr : expr EQ expr')
@pg.production('expr : expr LT expr')
@pg.production('expr : expr LE expr')
@pg.production('expr : expr GT expr')
@pg.production('expr : expr GE expr')
@pg.production('expr : expr NE expr')
def p_expr_relop(p):
    return (p[1].gettokentype(), (p[0], p[2]))

@pg.production('expr : expr AND expr')
@pg.production('expr : expr OR expr')
@pg.production('expr : NOT expr')
def p_expr_logic(p):
    if len(p) > 2:
        return (p[1].gettokentype(), (p[0], p[2]))
    else:
        return (p[0].gettokentype(), (p[1], ))

@pg.production('expr : LPAR expr RPAR')
def p_expr_parens(p):
    return ('PARENS', p[1])

@pg.production('expr : func')
@pg.production('expr : dict')
@pg.production('expr : list')
@pg.production('expr : slice')
@pg.production('expr : attrivar')
@pg.production('expr : variable')
@pg.production('expr : constant')
def p_expr_object(p):
    return p[0]

@pg.production('func : variable LPAR arglist RPAR')
@pg.production('func : attrivar LPAR arglist RPAR')
@pg.production('func : variable LPAR RPAR')
@pg.production('func : attrivar LPAR RPAR')
def p_func(p):
    if len(p) > 3:
        return ('FUNC', (p[0], p[2]))
    else:
        return ('FUNC', (p[0], ))

@pg.production('dict : LBRACE pairlist RBRACE')
@pg.production('dict : LBRACE RBRACE')
def p_dict(p):
    if len(p) > 2:
        return ('DICT', p[1])
    else:
        return ('DICT', {})

@pg.production('pairlist : pairlist COMMA pair')
@pg.production('pairlist : pair')
def p_pairlist(p):
    if len(p) > 1:
        key, value = p[2]
        p[0][key] = value
        return p[0]
    else:
        key, value = p[0]
        return {key: value}

@pg.production('pair : expr COLON expr')
@pg.production('pair : expr')
def p_pair(p):
    if len(p) > 1:
        return (p[0], p[2])
    else:
        return (p[0], None)

@pg.production('list : LSQB listexpr RSQB')
@pg.production('list : LSQB RSQB')
def p_list(p):
    if len(p) > 2:
        return ('LIST', p[1])
    else:
        return ('LIST', [])

@pg.production('listexpr : listexpr COMMA expr')
@pg.production('listexpr : expr')
def p_listexpr(p):
    if len(p) > 1:
        p[0].append(p[2])
        return p[0]
    else:
        return [p[0]]

@pg.production('slice : expr LSQB slicelist RSQB')
def p_slice(p):
    return ('SLICE', (p[0], p[2]))

@pg.production('slicelist : slicelist COMMA slicexpr')
@pg.production('slicelist : slicexpr')
def p_slicelist(p):
    if len(p) > 1:
        p[0].append(p[2])
        return p[0]
    else:
        return [p[0]]

@pg.production('slicexpr : expr COLON expr COLON expr')
@pg.production('slicexpr : expr COLON expr COLON')
@pg.production('slicexpr : expr COLON COLON expr')
@pg.production('slicexpr : expr COLON expr')
@pg.production('slicexpr : expr COLON COLON')
@pg.production('slicexpr : expr COLON')
@pg.production('slicexpr : expr')
@pg.production('slicexpr : COLON expr COLON expr')
@pg.production('slicexpr : COLON expr COLON')
@pg.production('slicexpr : COLON COLON expr')
@pg.production('slicexpr : COLON expr')
def p_slicexpr(p):
    return [item for item in p]

@pg.production('paralist : paralist COMMA parameter')
@pg.production('paralist : parameter')
def p_paralist(p):
    if len(p) > 1:
        _, items = p[0]
        items.append(p[2])
        return ('PARALIST', items)
    else:
        return ('PARALIST', [p[0]])

@pg.production('parameter : variable ASSIGN expr')
@pg.production('parameter : variable')
def p_parameter(p):
    if len(p) > 1:
        return (p[0], p[2])
    else:
        return (p[0], )

@pg.production('arglist : arglist COMMA argument')
@pg.production('arglist : argument')
def p_arglist(p):
    if len(p) > 1:
        _, items = p[0]
        items.append(p[2])
        return ('ARGLIST', items)
    else:
        return ('ARGLIST', [p[0]])

@pg.production('argument : variable ASSIGN expr')
@pg.production('argument : expr')
def p_argument(p):
    if len(p) > 1:
        return (p[0], p[2])
    else:
        return (p[0], )

@pg.production('varlist : varlist COMMA attrivar')
@pg.production('varlist : varlist COMMA variable')
@pg.production('varlist : attrivar')
@pg.production('varlist : variable')
def p_varlist(p):
    if len(p) > 1:
        _, items = p[0]
        items.append(p[2])
        return ('VARLIST', items)
    else:
        return ('VARLIST', [p[0]])

@pg.production('attrivar : func DOT variable')
@pg.production('attrivar : dict DOT variable')
@pg.production('attrivar : list DOT variable')
@pg.production('attrivar : slice DOT variable')
@pg.production('attrivar : attrivar DOT variable')
@pg.production('attrivar : variable DOT variable')
@pg.production('attrivar : constant DOT variable')
def p_attrivar(p):
    return ('ATTR', (p[0], p[2]))

@pg.production('variable : NAME')
def p_variable(p):
    return ('VARIABLE', p[0].getstr())

@pg.production('constant : NUMBER')
@pg.production('constant : STRING')
def p_constant(p):
    return (p[0].gettokentype(), eval(p[0].getstr()))

parser = pg.build()
