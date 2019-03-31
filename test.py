from dragon.dragonlexer import lexer
from dragon.dragonparser import parser
import pprint


code = '''\
#! /usr/bin/env dragon
我 = 123 % 1.23\\
I = 123 / 123j'''
print('```')
print(code)
print('```')
for token in lexer.lex(code):
    print(token, token.getsourcepos())

print('- ' * 32)
code = '''\
#! /usr/bin/env dragon
a = 1 + 1.1j
1 + 2^10
a
a * (b + c^2)
b = "abc\\n"
[['a', 'b', 'c'], [1, 2, 3]]
l = [['a', 'b', 'c'], [1, 2, 3], 1 + 2 + 3]
[2^1024, 1.25 + 5.21j]
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
