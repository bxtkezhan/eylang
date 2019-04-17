from .easylexer import reserved
from .easylexer import rules as lex_rules
from .easyinterpreter import *
from rply import ParserGenerator


EASY_VARS = {}

pg = ParserGenerator(
    list(reserved.values()) + [name for name, _ in lex_rules],
    precedence=[
        ('left', ['AND', 'OR', 'NOT']),
        ('left', ['EQ', 'LT', 'LE', 'GT', 'GE', 'NE']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV', 'MOD']),
        ('left', ['POWER']),
        ('right', ['SIGN']),
        ('left', ['LSQB', 'DOT']),
    ]
)

@pg.production('program : program statement')
@pg.production('program : statement')
def p_program(p):
    if len(p) == 1:
        line, stat = p[0]
        return Program({line: stat})
    elif len(p) == 2:
        line, stat = p[1]
        p[0].set(line, stat)
        return p[0]

@pg.production('statement : command NEWLINE')
def p_statement(p):
    return (p[1].getsourcepos().lineno, p[0])

@pg.production('statement : NEWLINE')
def p_statement_newline(p):
    return (p[0].getsourcepos().lineno, (p[0].gettokentype(), None))

@pg.production('command : IMPORT expr')
def p_command_return(p):
    return ('IMPORT', p[1])

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
        return IF(p[1], p[3], p[6])
    else:
        return IF(p[1], p[3])

@pg.production('command : varlist ASSIGN expr')
def p_command_assign(p):
    return Assign(p[0], p[2])

@pg.production('command : PUTS expr')
def p_command_puts(p):
    return Puts(p[1])

@pg.production('command : expr')
def p_command_expr(p):
    return Expr(p[0])

@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
@pg.production('expr : expr MOD expr')
@pg.production('expr : expr POWER expr')
@pg.production('expr : expr EQ expr')
@pg.production('expr : expr LT expr')
@pg.production('expr : expr LE expr')
@pg.production('expr : expr GT expr')
@pg.production('expr : expr GE expr')
@pg.production('expr : expr NE expr')
def p_expr_binop(p):
    return BinaryOp(p[1], p[0], p[2])

@pg.production('expr : PLUS expr', precedence='SIGN')
@pg.production('expr : MINUS expr', precedence='SIGN')
def p_expr_sign(p):
    return Sign(p[0], p[1])

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
    return Parens(p[1])

@pg.production('expr : func')
@pg.production('expr : dict')
@pg.production('expr : list')
@pg.production('expr : index')
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
        return Func(p[0], p[2])
    else:
        return Func(p[0])

@pg.production('dict : LBRACE pairlist RBRACE')
@pg.production('dict : LBRACE RBRACE')
def p_dict(p):
    if len(p) > 2:
        return Dictionary(p[1])
    else:
        return Dictionary()

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

@pg.production('list : LSQB exprlist RSQB')
@pg.production('list : LSQB RSQB')
def p_list(p):
    if len(p) > 2:
        return List(p[1])
    else:
        return List()

@pg.production('exprlist : exprlist COMMA expr')
@pg.production('exprlist : expr')
def p_exprlist(p):
    if len(p) > 1:
        p[0].append(p[2])
        return p[0]
    else:
        return [p[0]]

@pg.production('index : expr LSQB indexlist RSQB')
def p_index(p):
    return Index(p[0], p[2])

@pg.production('indexlist : indexlist COMMA indexexpr')
@pg.production('indexlist : indexexpr')
def p_indexlist(p):
    if len(p) > 1:
        p[0].append(p[2])
        return p[0]
    else:
        return [p[0]]

@pg.production('indexexpr : expr COLON expr COLON expr')
def p_indexexprc(p): return (p[0], p[2], p[4])
@pg.production('indexexpr : expr COLON expr COLON')
def p_indexexprb(p): return (p[0], p[2], None)
@pg.production('indexexpr : expr COLON COLON expr')
def p_indexexpra(p): return (p[0], None, p[3])
@pg.production('indexexpr : COLON expr COLON expr')
def p_indexexpr9(p): return (None, p[1], p[3])
@pg.production('indexexpr : COLON expr COLON')
def p_indexexpr8(p): return (None, p[1], None)
@pg.production('indexexpr : COLON COLON expr')
def p_indexexpr7(p): return (None, None, p[2])
@pg.production('indexexpr : expr COLON COLON')
def p_indexexpr6(p): return (p[0], None, None)
@pg.production('indexexpr : expr COLON expr')
def p_indexexpr5(p): return (p[0], p[2], None)
@pg.production('indexexpr : COLON COLON')
def p_indexexpr4(p): return (None, None, None)
@pg.production('indexexpr : expr COLON')
def p_indexexpr3(p): return (p[0], None, None)
@pg.production('indexexpr : COLON expr')
def p_indexexpr2(p): return (None, p[1], None)
@pg.production('indexexpr : COLON')
def p_indexexpr1(p): return (None, None, None)
@pg.production('indexexpr : expr')
def p_indexexpr0(p): return (p[0], )

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
        p[0].append(p[2])
        return p[0]
    else:
        return VarList([p[0]])

@pg.production('attrivar : expr DOT variable')
def p_attrivar(p):
    return Attribute(p[0], p[2], var_dict=EASY_VARS)

@pg.production('variable : NAME')
def p_variable(p):
    return Variable(p[0], var_dict=EASY_VARS)

@pg.production('constant : NUMBER')
@pg.production('constant : STRING')
def p_constant(p):
    return Constant(p[0])

parser = pg.build()
