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
def myfunc(x, y, z) then
    a = x

    if y then
        a = y
    end

    if z then
        a = z
    end

    return a
end

myfunc([1, 2], myfunc(), myfunc(10, 20, 30))

[1 * 10, (2, 3), [1, 2, 3]]
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
