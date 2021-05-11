from Token import Token


class NumberNode:
    def __init__(self, value):
        self.token: Token = value


class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.operator: Token = operator
        self.left = left
        self.right = right


class UnaryOpNode:
    def __init__(self, operator: Token, node):
        self.operator = operator
        self.node = node
