from rply import LexerGenerator
import tokenize


lg = LexerGenerator()

reserved = {v.lower(): v for v in [
    # 'IMPORT', 'PUTS', 'AND', 'OR', 'NOT', 'IF', 'ELIF', 'ELSE', 'END',
    'PUTS', 'AND', 'OR', 'NOT', 'IF', 'ELIF', 'ELSE', 'END',
    'WHILE', 'FOR', 'IN', 'DEF', 'RETURN']}

rules = [
    ['NUMBER', tokenize.Number],
    ['STRING', tokenize.String],
    ['NAME', tokenize.Name],
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
    ['LBRACE', r'\{'],
    ['RBRACE', r'\}'],
    ['EQ', r'=='],
    ['LE', r'<='],
    ['LT', r'<'],
    ['GE', r'>='],
    ['GT', r'>'],
    ['NE', r'!='],
    ['DOT', r'\.'],
    ['COMMA', r'\,'],
    ['COLON', r':'],
    ['ASSIGN', r'='],
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
