from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

lg = LexerGenerator()
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("NUMBER", r"\d+")
lg.add("NAME", r"\w+")
lg.add("EQUAL", r"=")

lg.ignore(r"\s+")

pg = ParserGenerator(
        ["NUMBER", "PLUS", "MINUS", "NAME", "EQUAL"],
        precedence=[
            ("left", ['EQUAL']),
            ("left", ['PLUS', 'MINUS'])])

global_vars = {}

@pg.production("main : expr")
def main(p):
    return p[0]

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
def expr_op(p):
    lhs = p[0].getint()
    rhs = p[2].getint()
    if p[1].gettokentype() == "PLUS":
        return BoxInt(lhs + rhs)
    elif p[1].gettokentype() == "MINUS":
        return BoxInt(lhs - rhs)
    else:
        raise AssertionError("This is impossible, abort the time machine!")

@pg.production("expr : NAME EQUAL expr")
def expr_assign(p):
    global_vars[p[0].getstr()] = p[2]
    return p[2]

@pg.production("expr : NUMBER")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))

@pg.production("expr : NAME")
def expr_name(p):
    return global_vars.get(p[0].getstr(), BoxInt(0))

lexer = lg.build()
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value

while True:
    user_input = input('>> ').strip()
    if user_input == 'EOF': break

    result = parser.parse(lexer.lex(user_input))
    print(result.getint())
