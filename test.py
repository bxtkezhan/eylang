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

    if x > y then
        a = y
    end

    if z then
        a = z
    end

    return a
end

myfunc([1, 2], myfunc(), myfunc(10, 20, 30))

[1 * 10, (2, 3), [1, 2, 3]]

a = 1 + 1 > 2 + 1

b = 1 + 1 > 2 + 1 and a - b < 3 + 4
c = 1 == 1

a = x
if a < 10 and a >= 1 then
    b = a^8
elif a < 100 then
    b = a^4
elif a < 1000 then
    b = a^2
else
    b = a
end
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
