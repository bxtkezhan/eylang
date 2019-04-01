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
def myfunc(a) then
    b = a - 100
    c = b * 100
    if a then
        c = a / 10
    end
    d = c^2
    def test() then
        a = 10
    end
end
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
