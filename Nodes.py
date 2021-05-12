from Token import Token
from typing import List


class StatementsNode:
    def __init__(self):
        self.stmt_list = []


class VarNode:
    def __init__(self, variable, value):
        self.variable: Token = variable
        self.value = value


class SymbolTable:
    sym_table: List[VarNode] = []


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
