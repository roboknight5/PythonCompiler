from Nodes import *
from Parser import Parser
from Lexer import Lexer
from CodeGenerator import CodeGenerator
from CodeOptimizer import CodeOptimizer


def print_tree(node, indent=""):
    # ├──
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
    elif isinstance(node, AssignNode):
        print(node.__class__.__name__, end="")
        print(" Value: " + node.variable.variable.value, end="")
    elif isinstance(node, VariableNode):
        print(node.__class__.__name__, end="")
        print(" Value: " + node.variable.value, end="")
    elif isinstance(node, IfStatementNode):
        print(node.__class__.__name__, end="")

    print()
    indent += "│   "
    if isinstance(node, BinaryOpNode):
        print_tree(node.left, indent)
        print(indent + node.operator.value)
        print_tree(node.right, indent)

    elif isinstance(node, UnaryOpNode):
        print_tree(node.node, indent)
    elif isinstance(node, NumberNode):
        pass
    elif isinstance(node, VariableNode):
        print_tree(node.value, indent)
    elif isinstance(node, AssignNode):
        if node.variable.value is not None:
            print_tree(node.variable, indent)
    elif isinstance(node, IfStatementNode):
        print(indent + "condition: ")
        print_tree(node.condition, indent)
        print(indent + "body: ")
        for body_stmt in node.body:
            print_tree(body_stmt, indent)


if __name__ == '__main__':
    file_input = open("input.txt")
    text = file_input.read()
    print("Lexer Output")
    lexer = Lexer(text)
    token_list = lexer.lex()

    parser = Parser(token_list)
    statement_list = parser.parse()
    print('Parser Before Optimization Output')
    for out in statement_list:
        print_tree(out)
    code_optimizer = CodeOptimizer()
    statement_list = code_optimizer.optimize(statement_list)
    code_generator = CodeGenerator(statement_list)
    print('Parser After Optimization Output')
    for out in statement_list:
        print_tree(out)
    code_generator.start()
    print('Code Generator Output')

    code_generator.print_instructions()
    file_output = open('output.txt', 'w')
    code_generator.write_instruction_to_file(file_output)
