from Nodes import *
from Parser import Parser
from Lexer import Lexer


def print_tree(node, indent=""):
    marker = "├──"
    print(indent, end="")
    print(marker, end="")
    if isinstance(node, BinaryOpNode):
        print(node.__class__.__name__, end="")
    elif isinstance(node, NumberNode):
        print(node.__class__.__name__, end="")
        print(" Value: " + node.token.value, end="")
    elif isinstance(node, UnaryOpNode):
        print(node.__class__.__name__, end="")
        print(" Operator: " + node.operator.value, end="")
    print()
    indent += "│   "
    if isinstance(node, BinaryOpNode):
        print_tree(node.left, indent)
        print(indent + node.operator.value)
        print_tree(node.right, indent)

    elif isinstance(node, UnaryOpNode):
        print_tree(node.node,indent)
    elif isinstance(node, NumberNode):
        pass


if __name__ == '__main__':
    file = open("input.txt")
    text = file.read()

    lexer = Lexer(text)
    token_list = lexer.lex()

    parser = Parser(token_list)
    out = parser.parse()
    print_tree(out)
