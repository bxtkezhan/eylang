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
#! /usr/bin/env dragon

def myfunc(a, b, k=10)
    c = a + b
    c = c * k
    return c
end

list = [1, 2, 3]
list = list + [1, 2, 3]
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
