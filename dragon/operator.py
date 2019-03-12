from rply.token import BaseBox


class OneOp(BaseBox):
    def __init__(self, x):
        self.x = x

class Positive(OneOp):
    def eval(self):
        return + self.x.eval()

class Negative(OneOp):
    def eval(self):
        return - self.x.eval()

class BinaryOp(BaseBox):
    def __init__(self, x0, x1):
        self.x0 = x0
        self.x1 = x1

class Add(BinaryOp):
    def eval(self):
        return self.x0.eval() + self.x1.eval()

class Sub(BinaryOp):
    def eval(self):
        return self.x0.eval() - self.x1.eval()

class Mul(BinaryOp):
    def eval(self):
        return self.x0.eval() * self.x1.eval()

class Div(BinaryOp):
    def eval(self):
        return self.x0.eval() / self.x1.eval()
