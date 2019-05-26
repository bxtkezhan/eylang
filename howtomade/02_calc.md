# 开发自己的编程语言 —— 计算器（一）

今天我们借用一个计算器项目来学习如何使用rply库。这里所谓的计算器是一个支持加减运算的解释器程序，可以很简单的让我们学会使用rply构建简单的词法和语法分析器。

## 代码清单

```python
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

lg = LexerGenerator()
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("NUMBER", r"\d+")

lg.ignore(r"\s+")

pg = ParserGenerator(["NUMBER", "PLUS", "MINUS"],
        precedence=[("left", ['PLUS', 'MINUS'])], cache_id="myparser")

@pg.production("main : expr")
def main(p):
    return p[0]

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
def expr_op(p):
    lhs = p[0].getint()
    rhs = p[2].getint()
    if p[1].gettokentype() == "PLUS":
        return BoxInt(lhs + rhs)
    elif p[1].gettokentype() == "MINUS":
        return BoxInt(lhs - rhs)
    else:
        raise AssertionError("This is impossible, abort the time machine!")

@pg.production("expr : NUMBER")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))

lexer = lg.build()
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value
```

## 代码解释

1、开始编写之前我们要引入需要的模块。

```python
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
```

其中`LexerGenerator`用于构建词法解析器；`ParserGenerator`用于构建语法分析器；`BaseBox`用于构建语法树。

2、一般来说我们会先构建一个词法解析器，它会帮我们把代码中的内容解析成单个单个的Token对象，例如`1 + 2`可以被解析成[NUMBER, PLUS, NUMBER]。

```python
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
```
运行输出：
```bash
Token('NUMBER', '1')
Token('PLUS', '+')
Token('NUMBER', '1')
```

在上面的代码中先使用`lg = LexerGenerator()`实例一个对象，然后用`add`属性方法添加规则，`add`方法的第一个参数是Token的类型，第二个是正则表达式规则，如果有代码被正则表达式匹配，就会生成一个对应的Token对象而对象的类型则由第一个参数决定。

`lg.ignore(r"\s+")`则是用于忽略一些代码内容，一般会设置成忽略空格等空白字符。


最后使用`lexer = lg.build()`构建解析器。

在使用的时候传入代码字符串到`lexer`的属性方法`lex`就会得到一个生成器对象，可以用for语句取出Token对象。

3、