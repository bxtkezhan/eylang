from dragon.dragonlexer import lexer
from dragon.dragonparser import parser
import pprint


code = '''\
#! /usr/bin/env dragon
我 = 123 % 1.23\\
{}
I = 123 / 123j'''
print('```')
print(code)
print('```')
for token in lexer.lex(code):
    print(token, token.getsourcepos())

print('- ' * 32)
code = '''\
def myfunc(a, b=3, c=5)
    return a + b + c
end

for i in range(0, 100, step=3)
    puts myfunc(a=1, b=2, 3)
else
    a = 1 + 1
end
a = [1, [1, [1, 2, 3], 3], 3]

10 * [10, 10]
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
