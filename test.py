from dragon.dragonlexer import lexer
from dragon.dragonparser import parser
import pprint


code = '''\
#! /usr/bin/env dragon
我 = 123 % 1.23\\
{}
.
I = 123 / 123j'''
print('```')
print(code)
print('```')
for token in lexer.lex(code):
    print(token, token.getsourcepos())

print('- ' * 32)
code = '''\
a = 100 + myfunc(10, 20).x.float() + myfunc(100, 200).y.float() * 10
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
