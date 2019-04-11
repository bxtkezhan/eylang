from easy.easylexer import lexer
from easy.easyparser import parser
import pprint


code = '''\
#!/usr/bin/env eylang
import 'math.ey'

def myfunc(x, y, k=10)
    x = x * k
    y = y * k
    return vector2d(x, y)
end

matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

a = 100 + myfunc(10, 20).x.float() + myfunc(100, 200).y.float() * 10
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))

print('- ' * 32)

code = '''\
a, b, c = "abc"
k = a * 10 + "-" + b * 10 + "-" + c * 10 + "-" + (a + b + c) * 10
k
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
print('\nresult:')
print(parser.parse(lexer.lex(code)).eval())
