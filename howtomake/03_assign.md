# 开发自己的编程语言 —— 变量与赋值

今天我们来给计算器添加变量和变量赋值功能。

## BaseBox

在讲解新的代码前我们先仔细研究一下rply的BaseBox对象，我们先看看BaseBox的定义：

```python
class BaseBox(object):
    """
    A base class for polymorphic boxes that wrap parser results. Simply use
    this as a base class for anything you return in a production function of a
    parser. This is necessary because RPython unlike Python expects functions
    to always return objects of the same type.
    """
    _attrs_ = []
```

以上就是rply项目中的BaseBox定义，是不是感觉在闹着玩，整个类中只有一个被初始为空列表的属性变量`_attrs_`，所以其实BaseBox并没有直接为我们做什么，原则上之前代码中的BoxInt类其实是不需要继承BaseBox的。

如果你愿意继续阅读更多的rply源代码就会发现其实rply为我们做的并没有多少，事实上rply中的内容我们完全可以自己花时间来完成并且在大多数时候不会遇到困难。这样有一个好处就是我们可以握有开发项目的主动权，当我们不满意它的功能时我们就自己动手做，这一点也是我在开发eylang和编写教程时使用rply的重要原因。

## 代码清单

```python
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

lg = LexerGenerator()
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("NUMBER", r"\d+")
lg.add("NAME", r"\w+")
lg.add("EQUAL", r"=")

lg.ignore(r"\s+")

pg = ParserGenerator(
        ["NUMBER", "PLUS", "MINUS", "NAME", "EQUAL"],
        precedence=[
            ("left", ['EQUAL']),
            ("left", ['PLUS', 'MINUS'])])

global_vars = {}

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

@pg.production("expr : NAME EQUAL expr")
def expr_assign(p):
    global_vars[p[0].getstr()] = p[2]
    return p[2]

@pg.production("expr : NUMBER")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))

@pg.production("expr : NAME")
def expr_name(p):
    return global_vars.get(p[0].getstr(), BoxInt(0))

lexer = lg.build()
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value

while True:
    user_input = input('>> ').strip()
    if user_input == 'EOF': break

    result = parser.parse(lexer.lex(user_input))
    print(result.getint())
```

## 代码解释

1、我们又定义了两条词法检测规则用于检测变量名和等于号：

```python
lg.add("NAME", r"\w+")
lg.add("EQUAL", r"=")
```

2、定义词法检测规则后，将Token名称添加到语法解析器生成工具中：

```python
pg = ParserGenerator(
        ["NUMBER", "PLUS", "MINUS", "NAME", "EQUAL"],
        precedence=[
            ("left", ['EQUAL']),
            ("left", ['PLUS', 'MINUS'])])
```

我们注意到代码中有新的优先级规则`("left", ['EQUAL'])`位于`("left", ['PLUS', 'MINUS'])`之前，这表明赋值操作的优先级低于加减操作。

3、初始化一个字典对象用于存储变量：

```python
global_vars = {}
```

之所以选择字典对象是因为我们需要同时保存变量的名称以及值，用字典来做很方便。

4、现在我们定义赋值语法规则并实现对应的方法：

```python
@pg.production("expr : NAME EQUAL expr")
def expr_assign(p):
    global_vars[p[0].getstr()] = p[2]
    return p[2]
```

我们定义的规则是"expr : NAME EQUAL expr"，以输入代码`num = 1 + 1`为例，num、=被匹配并分别包装成类型为NAME、EQUAL的Token对象，expr就是表达式`1 + 1`。在接下来的方法expr_assign中，`p[0].getstr()`会取出匹配到的第一个Token的字面值并将其作为变量名。变量值就是`p[2]`，即表达式的结果，是一个BoxInt对象。完成赋值操作` global_vars[p[0].getstr()] = p[2]`后我们还将变量值返回`return p[2]`。

5、最后我们还需要定义一条语法解析规则直接解析变量并返回成表达式，这样我们就可以在计算过程中使用变量并且方便随时查看：

```python
@pg.production("expr : NAME")
def expr_name(p):
    return global_vars.get(p[0].getstr(), BoxInt(0))
```

大功告成，我们开始运行吧(ゝ∀･)！