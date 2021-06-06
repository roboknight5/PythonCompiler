from Token import Token
from typing import List


class NumberNode:
    def __init__(self, value):
        self.token: Token = value


class VariableNode:
    def __init__(self, variable, value):
        self.variable: Token = variable
        self.value = value


class SymbolTable:
    symbol_table: List[VariableNode] = []


class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.operator: Token = operator
        self.left = left
        self.right = right


class UnaryOpNode:
    def __init__(self, operator: Token, node):
        self.operator = operator
        self.node = node


class AssignNode:
    def __init__(self, variable):
        self.variable: VariableNode = variable


class IfStatementNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
