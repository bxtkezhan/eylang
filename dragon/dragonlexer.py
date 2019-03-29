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
    ['POW', r'\^'],
    ['DIV', r'/'],
    ['MOD', r'%'],
    ['LPAREN', r'\('],
    ['RPAREN', r'\)'],
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

lexer = lg.build()
