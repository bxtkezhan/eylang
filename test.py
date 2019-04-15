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
a[::1][:1][0]
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))

print('- ' * 32)

code = '''\
vect2d = {}
vect2d.x = 10
vect2d.y = 10
vect2d.x + vect2d.y
puts 'hello world'
puts (3 + 2j) * 5
puts vect2d
puts -1 * 100
puts 1 --- 1 + 1
x, y = [1, 2]
puts [x, y]
a, b, c = [2^10, 1 + 10j, [1, 2, 3]]
l = [0, 1, 2, 3, 4, 5, 'a', 'b', 'c']
puts a
puts b
puts c
puts l[5]
puts l[3:8]
puts l[3:-1]
puts l[3::-1]
puts l[8:3:-1]
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
print('```')
parser.parse(lexer.lex(code)).eval()
print('```')
