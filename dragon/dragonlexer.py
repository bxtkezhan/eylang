from rply import LexerGenerator
import tokenize


lg = LexerGenerator()

reserved = {v.lower(): v for v in [
    'PUTS', 'AND', 'OR', 'NOT', 'IF', 'THEN', 'ELIF', 'ELSE', 'END',
    'WHILE', 'FOR', 'IN', 'DEF', 'RETURN']}

rules = [
    ['NUMBER', tokenize.Number],
    ['STRING', tokenize.String],
    ['NAME', tokenize.Name],
    ['ASSIGN', r'='],
    ['PLUS', r'\+'],
    ['MINUS', r'-'],
    ['MUL', r'\*'],
    ['POWER', r'\^'],
    ['DIV', r'/'],
    ['MOD', r'%'],
    ['LPAR', r'\('],
    ['RPAR', r'\)'],
    ['LSQB', r'\['],
    ['RSQB', r'\]'],
    ['EQ', r'=='],
    ['LT', r'<'],
    ['LE', r'<='],
    ['GT', r'>'],
    ['GE', r'>='],
    ['NE', r'!='],
    ['COMMA', r'\,'],
    ['SEMI', r';'],
    ['COLON', r':'],
    ['NEWLINE', '\n']]

for name, regex in rules:
    lg.add(name, regex)

lg.ignore(tokenize.group(r'\\\r?\n', r'[ \f\t]+', tokenize.Comment))

class DragonLexer:
    def __init__(self):
        self.lexer = lg.build()

    def lex(self, code):
        tokens = self.lexer.lex(code)
        while True:
            token = next(tokens)
            tokentype = token.gettokentype()
            if tokentype == 'NAME':
                token.name = reserved.get(token.getstr(), tokentype)
            yield token

lexer = DragonLexer()
