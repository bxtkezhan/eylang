# 开发自己的编程语言 —— 计算器

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

1、开始编写之前我们要引入需要的模块：

```python
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
```

其中`LexerGenerator`用于构建词法解析器；`ParserGenerator`用于构建语法分析器；`BaseBox`用于构建语法树。

2、一般来说我们会先构建一个词法解析器，它会帮我们把代码中的内容解析成单个单个的Token对象，例如`1 + 2`可以被解析成[NUMBER, PLUS, NUMBER]：

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

3、接下来我们要语法解析部分，我们先创建一个语法解析器对象：

```python
pg = ParserGenerator(["NUMBER", "PLUS", "MINUS"],
        precedence=[("left", ['PLUS', 'MINUS'])], cache_id="myparser")
```

第一个参数是一个列表，放入我们在`lg.add`中添加的Token的名称，目前有NUMBER、PLUS、MINUS这三个，接下来的`precedence`用于指定优先级，一般用于指定运算符优先级，当前的运算符只有PLUS、MINUS两个而且等级一样，所以就放在一起，`"left"`表示左优先级模式。`cache_id`用于设定缓存区的ID，这是rply库中的可选项。

4、接下来我们来看一下`ParserGenerator`的运作流程，我们以`1 + 1`代码为例：

首先我们的代码会被解析成的几个Token对象，分别是Token('NUMBER', '1') 、Token('PLUS', '+')、Token('NUMBER', '1')；

然后我们的程序开始构建表达式，当遇到Token('NUMBER', '1')对象时就会使用下面的代码进行解析：

```python
@pg.production("expr : NUMBER")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))
```

装饰器`@pg.production`中定义了这样的规则`expr: NUMBER`，即如果遇到NUMBER就将其转为expr表达式，而对应执行的方法是`expr_num`，方法的参数p用于接收规则中`:`后的参数序列，例如当前只有一个NUMBER，则是[Token('NUMBER', '1')]，`BoxInt(int(p[0].getstr()))`则是先将Token的字符内容取出然后转为int类型并传入BoxInt类进行实例化；

有了数字构成的表达式我们就可以开始进行计算：

```python
@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
```
我们先定义规则`expr : expr PLUS expr`和`expr : expr MINUS expr`，当我们遇到对应的表达式的时候就执行解析操作，规则中的expr可以是由`expr : NUMBER`解析后生成的，也可以是由`expr : expr PLUS expr`、`expr : expr MINUS expr`解析后生成的。

指定规则后，我们来看看如何具体的构建方法：

```python
def expr_op(p):
    lhs = p[0].getint()
    rhs = p[2].getint()
    if p[1].gettokentype() == "PLUS":
        return BoxInt(lhs + rhs)
    elif p[1].gettokentype() == "MINUS":
        return BoxInt(lhs - rhs)
    else:
        raise AssertionError("This is impossible, abort the time machine!")
```

我们定义了`expr_op`方法，根据我们定义的规则这时的参数p是一个具有三个元素的序列对象可能是[expr, PLUS, expr]也可能是[expr, MINUS, expr]，所以我们可以判断下标0和2的一定是BoxInt对象，因为我们之前用`expr_num`方法做了转化，那么现在我们可以用BoxInt中的`getint`属性方法获取值。得到数值之后我们对`p[1]`进行判断，PLUS和MINUS的表达符号目前还没有解析过所以仍旧是Token对象，我们用`gettokentype`方法得到类型并进行判断，然后给出对应的输出，如果是PLUS就用`return BoxInt(lhs + rhs)`，如果是MINUS就用`return BoxInt(lhs - rhs)`，否则就抛出异常`AssertionError`。

完成计算规则和解析后我们要指定一个最终或者称为顶层节点解析的规则：

```python
@pg.production("main : expr")
def main(p):
    return p[0]
```

5、定义好规则和解析方法后我们就可以完成构建了：`parser = pg.build()`，构建好的`parser`可以使用`parse`方法直接解析`lexer.lex`方法的返回内容，所以一般我们可以写成`parser.parse(lexer.lex(code_str))`。

6、现在我们来商量一下怎么使用，我们已经有了代码清单，还需要准备一些什么？也许我们需要获得用户输入，然后对输入进行解析，那么我们就添加如下代码：

```python
while True:
    user_input = input('>> ').strip()
    if user_input == 'EOF': break

    result = parser.parse(lexer.lex(user_input))
    print(result.getint())
```

大功告成，我们开始运行吧(ゝ∀･)！