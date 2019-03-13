from rply.token import BaseBox


class Value(BaseBox):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

class ListStack(BaseBox):
    def __init__(self, data):
        self.sequence = [data]

    def append(self, data):
        self.sequence.append(data)

    def eval(self):
        return self.sequence

    def tovalue(self):
        return Value(self.sequence)
