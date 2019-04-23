from eylang.eylanglexer import lexer
from eylang.eylangparser import parser, EYLANG_VARS
import pprint


code = '''\
def f1(a)
    a = 1 + a
    b = 2
    puts 'locals:'
    puts locals
    puts 'globals:'
    puts globals

    def f2(b)
        b = 2 + b
        c = 4
        puts 'locals:'
        puts locals
        puts 'globals:'
        puts globals
        return [b, c]
    end
    puts f2(b=b)

    return [a, b]
end

a = 1
puts a
puts f1(a=a)
puts a
'''
print('```')
print(code)
print('```')
pprint.pprint((parser.parse(lexer.lex(code))))
print('```')
parser.parse(lexer.lex(code)).eval()
print('```')
