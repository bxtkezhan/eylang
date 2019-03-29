from dragon.dragonlexer import lexer
from dragon.dragonparser import parser
import json


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

123

432
1024j
'''
print('```')
print(code)
print('```')
tree = json.dumps(parser.parse(lexer.lex(code)), ensure_ascii=False, indent=2, sort_keys=True)
print(tree)
