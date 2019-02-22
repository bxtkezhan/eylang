from dragon.interpreter import lexer, parser

print(parser.parse(lexer.lex('1 + 1')).eval())
print(parser.parse(lexer.lex('1 + 2 * 3')).eval())
# print(parser.parse(lexer.lex('1 1')).eval())
