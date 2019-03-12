from rply.token import BaseBox


class Value(BaseBox):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data
