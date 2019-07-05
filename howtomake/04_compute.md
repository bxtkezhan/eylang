# 开发自己的编程语言 —— 完善数字计算

今天我们来丰富一下数字计算功能并学习一些有助于后期开发的Python技巧。在本节当中我们将实现整数、浮点、复数的四则运算以及取模、指数、符号设置、括号优先等操作。

## 代码清单

```python
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
import tokenize
import operator
import readline


global_vars = {}

lg = LexerGenerator()

rules = [
    ['NUMBER', tokenize.Number],
    ['NAME', tokenize.Name],
    ['PLUS', r'\+'],
    ['MINUS', r'-'],
    ['MUL', r'\*'],
    ['POWER', r'\^'],
    ['DIV', r'/'],
    ['MOD', r'%'],
    ['LPAR', r'\('],
    ['RPAR', r'\)'],
    ['ASSIGN', r'=']]

for name, regex in rules:
    lg.add(name, regex)

lg.ignore(r'\s+')

pg = ParserGenerator(
    [name for name, _ in rules],
    precedence=[
        ('left', ['ASSIGN']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV', 'MOD']),
        ('left', ['POWER']),
        ('right', ['SIGN']),
    ]
)

@pg.production('main : expr')
def main(p):
    return p[0]

@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
@pg.production('expr : expr MOD expr')
@pg.production('expr : expr POWER expr')
def expr_op(p):
    ops = {
        'PLUS': operator.add,
        'MINUS': operator.sub,
        'MUL': operator.mul,
        'DIV': operator.truediv,
        'MOD': operator.mod,
        'POWER': operator.pow
    }

    lhs = p[0].getvalue()
    rhs = p[2].getvalue()
    opt = ops.get(p[1].gettokentype())
    if opt: return BoxNumber(opt(lhs, rhs))

    raise AssertionError('This is impossible, abort the time machine!')

@pg.production('expr : PLUS expr', precedence='SIGN')
@pg.production('expr : MINUS expr', precedence='SIGN')
def expr_sign(p):
    num = p[1].getvalue()
    if p[0].gettokentype() == 'PLUS':
        return BoxNumber(num)
    else:
        return BoxNumber(-num)

@pg.production('expr : LPAR expr RPAR')
def expr_pars(p):
    return p[1]

@pg.production('expr : NAME ASSIGN expr')
def expr_assign(p):
    global_vars[p[0].getstr()] = p[2]
    return p[2]

@pg.production('expr : NUMBER')
def expr_num(p):
    return BoxNumber(eval(p[0].getstr()))

@pg.production('expr : NAME')
def expr_name(p):
    return global_vars.get(p[0].getstr(), BoxNumber(0))

lexer = lg.build()
parser = pg.build()

class BoxNumber(BaseBox):
    def __init__(self, value):
        self.value = value

    def getvalue(self):
        return self.value

while True:
    try:
        user_input = input('>> ').strip()
    except EOFError: break

    if user_input:
        result = parser.parse(lexer.lex(user_input))
        print(result.getvalue())
```

## 代码解释

1、我们先将词法规则写入一个列表，然后遍历插入，这样方便我们重复使用：

```python
rules = [
    ['NUMBER', tokenize.Number],
    ['NAME', tokenize.Name],
    ['PLUS', r'\+'],
    ['MINUS', r'-'],
    ['MUL', r'\*'],
    ['POWER', r'\^'],
    ['DIV', r'/'],
    ['MOD', r'%'],
    ['LPAR', r'\('],
    ['RPAR', r'\)'],
    ['ASSIGN', r'=']]

for name, regex in rules:
    lg.add(name, regex)
```

其中的`tokenize.Number`、`tokenize.Name`是Python当中默认定义的词法匹配规则。

2、定义词法检测规则后，将Token名称添加到语法解析器生成工具中并定义优先级：

```python
pg = ParserGenerator(
    [name for name, _ in rules],
    precedence=[
        ('left', ['ASSIGN']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV', 'MOD']),
        ('left', ['POWER']),
        ('right', ['SIGN']),
    ]
)
```

这里我们可以直接将之前写入rules当中的Token名称取出来而不必重复编辑。

3、添加基础运算语法规则并实现对应的方法：

```python
@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
@pg.production('expr : expr MOD expr')
@pg.production('expr : expr POWER expr')
def expr_op(p):
    ops = {
        'PLUS': operator.add,
        'MINUS': operator.sub,
        'MUL': operator.mul,
        'DIV': operator.truediv,
        'MOD': operator.mod,
        'POWER': operator.pow
    }

    lhs = p[0].getvalue()
    rhs = p[2].getvalue()
    opt = ops.get(p[1].gettokentype())
    if opt: return BoxNumber(opt(lhs, rhs))

    raise AssertionError('This is impossible, abort the time machine!')
```

在这里我们并没有使用`if-elif-else`来进行判断，而是将操作名称和operator当中的对应的方法做成字典来索引选取需要的操作。

4、定义并实现符号变换的规则与方法：

```python
@pg.production('expr : PLUS expr', precedence='SIGN')
@pg.production('expr : MINUS expr', precedence='SIGN')
def expr_sign(p):
    num = p[1].getvalue()
    if p[0].gettokentype() == 'PLUS':
        return BoxNumber(num)
    else:
        return BoxNumber(-num)
```

注意到装饰器中的`precedence='SIGN'`这表示虽然我们虽然在规则中匹配的符号是PLUS、MINUS但是优先级参考SIGN。

5、定义并实现括号优先运算的规则与方法：

```python
@pg.production('expr : LPAR expr RPAR')
def expr_pars(p):
    return p[1]
```

6、由于目前我们的NUMBER可以匹配整数、浮点、虚数，所以要更换解析方式，最简单的方法就是`eval`：

```python
@pg.production('expr : NUMBER')
def expr_num(p):
    return BoxNumber(eval(p[0].getstr()))
```

7、BoxInt也应该改为BoxNumber，对应的getint方法也改成getvalue：

```python
class BoxNumber(BaseBox):
    def __init__(self, value):
        self.value = value

    def getvalue(self):
        return self.value
```

8、我们用EOFError异常检测来替代之前的用户EOF字符输入检测，这样可以用`<Ctrl-D>`来进行中断：

```python
while True:
    try:
        user_input = input('>> ').strip()
    except EOFError: break
    ... ...
```

9、另外我们还引入readline模块帮助优化用户体验：`import readline`，这样可以使用上下方向键选择历史输入记录。

大功告成，我们开始运行吧(ゝ∀･)！