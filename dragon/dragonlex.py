from rply import LexerGenerator
import tokenize

lg = LexerGenerator()

reserved = {v.lower(): v for v in [
    'PUTS', 'AND', 'OR', 'NOT', 'IF', 'THEN', 'ELIF', 'ELSE', 'END',
    'WHILE', 'FOR', 'IN', 'DEF', 'RETURN']}

lg.add('IMAG', tokenize.Imagnumber)
lg.add('FLOAT', tokenize.Floatnumber)
lg.add('INTEGER', tokenize.Intnumber)
lg.add('STRING', tokenize.String)
lg.add('NAME', tokenize.Name)
lg.add('ASSIGN', r'=')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('TIMES', r'\*')
lg.add('POWER', r'\^')
lg.add('DIVIDE', r'/')
lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.add('EQ', r'==')
lg.add('LT', r'<')
lg.add('LE', r'<=')
lg.add('GT', r'>')
lg.add('GE', r'>=')
lg.add('NE', r'!=')
lg.add('COMMA', r'\,')
lg.add('SEMI', r';')
lg.add('COLON', r':')
lg.add('NEWLINE', '\n')

lg.ignore(tokenize.group(r'\\\r?\n', r'[ \f\t]+', tokenize.Comment))

lexer = lg.build()

if __name__ == '__main__':
    code = '''\
#! /usr/bin/env dragon
我 = 123 + 1.23\\
I = 123 + 123j'''

    print('```')
    print(code)
    print('```')
    tokens = lexer.lex(code)
    for token in tokens:
        print(token, token.getsourcepos())
