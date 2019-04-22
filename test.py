from eylang.eylanglexer import lexer
from eylang.eylangparser import parser
import pprint


code = '''\
#!/usr/bin/env eylang
# import 'math.ey'

def myfunc(x, y, k=10)
    x = x * k
    y = y * k
    return vector2d(x, y)
end

matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

a = 100 + myfunc(10, 20).x.float() + myfunc(100, 200).y.float() * 10
-1 * myfunc()
1 +++1 + 1
a + a[::1][:1][0]
return 1
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))

print('- ' * 32)

code = '''\
def myfunc(a=1, b=10, c=100)
    puts a
    puts b
    puts c
    return a + b + c
end

puts myfunc(10^2, 20, b=100 ^ 0.5, c=1)
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
print('```')
parser.parse(lexer.lex(code)).eval()
print('```')
