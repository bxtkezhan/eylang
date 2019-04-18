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
-1 * myfunc()
1 +++1 + 1
a + a[::1][:1][0]
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))

print('- ' * 32)

code = '''\
for i, j in [[1, 2], [2, 3], [3, 4]]
    puts [i, j]
else
    puts [i, j]
end
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
print('```')
parser.parse(lexer.lex(code)).eval()
print('```')
