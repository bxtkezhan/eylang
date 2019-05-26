from rply import LexerGenerator

lg = LexerGenerator()
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("NUMBER", r"\d+")

lg.ignore(r"\s+")
lexer = lg.build()

mycode = '1 + 1'
mytoken = lexer.lex(mycode)
for token in mytoken:
    print(token)
