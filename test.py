from dragon.interpreter import lexer, parser

def runline(code):
    print(parser.parse(lexer.lex(code)).eval())

runline('1 + 2 * 3')
runline('1.5 + 2 * 3')
runline('1 + 1j')
runline('"abc abc$\\nabc"')
runline('"abc " * 3 + "efg"')
runline('a = 1 + 1')
runline('a + a * 200')
runline('c = b = "1024a"')
runline('b * 2')
runline('c')
runline('--+-+1')
runline('a = c = b = a')
runline('my_var = 1024')
runline('my_var2 = my_var * 1024')
# runline('1 1')
