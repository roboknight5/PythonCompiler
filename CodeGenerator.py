from Nodes import *
from Token import *


class CodeGenerator:
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list
        self.constants = []
        self.constant_instructions = []

        self.symbol_table = {}

        self.temp_count = 0

        self.instructions = []

        self.variables = []
        self.variable_instructions = []

        self.label_count = 0
        self.exit_label_count = 0
        self.instruction_prefix = "\t"

    def start(self):
        self.instructions.append('PROGRAM START 0')
        first_instruction = True
        for x in self.stmt_list:
            if first_instruction: self.instruction_prefix = "FIRST "
            self.__generate(x)
            first_instruction = False

        self.__optimize_assembly()

    def __optimize_assembly(self):
        for idx, var in enumerate(self.instructions):
            instruction = var.split()
            if len(instruction) >= 3:
                instruction = instruction[1:]
            if instruction[0] == "STA":
                sta_value = instruction[1]
                if idx + 1 < len(self.instructions):
                    next_instruction = self.instructions[idx + 1].split()
                    if next_instruction[1] == sta_value:
                        del self.instructions[idx + 1]
            if instruction[0] == "J":
                exit_label_found = False
                j_value = instruction[1]
                instructions_after_j = self.instructions[idx:]
                for x in instructions_after_j:
                    inst = x.split()
                    if inst[0] == j_value:
                        exit_label_found = True
                if not exit_label_found:
                    if "0" not in self.constants:
                        self.constant_instructions.append(f"WORD CONST_{0} {0}")
                        self.symbol_table["0"] = f"CONST_{0}"
                        self.constants.append("0")
                    zero = "0"
                    self.instructions.append(f"{j_value} LDA {self.symbol_table.get(zero)}")

    def __generate(self, node):
        if isinstance(node, BinaryOpNode):
            left = self.__generate(node.left)
            right = self.__generate(node.right)
            if node.operator.kind == TokenKind.PlusToken:
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(left)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}ADD {self.symbol_table.get(right)}")
                self.instructions.append(f"{self.instruction_prefix}STA TEMP_{self.temp_count}")
                temp = f"TEMP_{self.temp_count}"
                self.symbol_table[temp] = temp
                self.temp_count += 1
                return temp

            elif node.operator.kind == TokenKind.MinusToken:
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(left)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}SUB {self.symbol_table.get(right)}")
                self.instructions.append(f"{self.instruction_prefix}STA TEMP_{self.temp_count}")
                temp = f"TEMP_{self.temp_count}"
                self.symbol_table[temp] = temp
                self.temp_count += 1
                return temp

            elif node.operator.kind == TokenKind.AsteriskToken:
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(left)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}MUL {self.symbol_table.get(right)}")
                self.instructions.append(f"{self.instruction_prefix}STA TEMP_{self.temp_count}")
                temp = f"TEMP_{self.temp_count}"
                self.symbol_table[temp] = temp
                self.temp_count += 1
                return temp
            elif node.operator.kind == TokenKind.SlashToken:
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(left)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}DIV {self.symbol_table.get(right)}")
                self.instructions.append(f"{self.instruction_prefix}STA TEMP_{self.temp_count}")
                temp = f"TEMP_{self.temp_count}"
                self.symbol_table[temp] = temp
                self.temp_count += 1
                return temp
            elif node.operator.kind == TokenKind.EqualEqualToken:
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(left)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}COMP {self.symbol_table.get(right)}")
                self.instructions.append(f"{self.instruction_prefix}JEQ LABEL_{self.label_count}")
                self.instructions.append(f"{self.instruction_prefix}J EXIT_{self.exit_label_count}")
            elif node.operator.kind == TokenKind.GreaterThanToken:
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(left)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}COMP {self.symbol_table.get(right)}")
                self.instructions.append(f"{self.instruction_prefix}JGT LABEL_{self.label_count}")
                self.instructions.append(f"{self.instruction_prefix}J EXIT_{self.exit_label_count}")
            elif node.operator.kind == TokenKind.SmallerThanToken:
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(left)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}COMP {self.symbol_table.get(right)}")
                self.instructions.append(f"{self.instruction_prefix}JLT LABEL_{self.label_count}")
                self.instructions.append(f"{self.instruction_prefix}J EXIT_{self.exit_label_count}")

        if isinstance(node, NumberNode):
            if node.token.value not in self.constants:
                instruction = f"WORD CONST_{node.token.value} {node.token.value}"
                self.constant_instructions.append(instruction)
                self.constants.append(node.token.value)
                self.symbol_table[node.token.value] = f"CONST_{node.token.value}"
            return node.token.value

        if isinstance(node, UnaryOpNode):
            operand = self.__generate(node.node)
            if node.operator.kind == TokenKind.MinusToken:
                if "0" not in self.constants:
                    self.constant_instructions.append(f"WORD CONST_{0} {0}")
                    self.symbol_table["0"] = f"CONST_{0}"
                    self.constants.append("0")

                zero = "0"
                self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(zero)}")
                self.instruction_prefix = "\t"
                self.instructions.append(f"{self.instruction_prefix}SUB {self.symbol_table.get(operand)}")
                self.instructions.append(f"{self.instruction_prefix}STA TEMP_{self.temp_count}")
                temp = f"TEMP_{self.temp_count}"
                self.symbol_table[temp] = temp
                self.temp_count += 1
                return temp

        if isinstance(node, VariableNode):
            return node.variable.value

        if isinstance(node, AssignNode):
            if node.variable.variable.value not in self.variables:
                self.variable_instructions.append(f"RESW {node.variable.variable.value} 1")
                self.symbol_table[node.variable.variable.value] = node.variable.variable.value
                self.variables.append(node.variable.variable.value)

            if node.variable.value is not None:
                operand = self.__generate(node.variable.value)

                if isinstance(node.variable.value, NumberNode) or isinstance(node.variable.value, VariableNode):
                    self.instructions.append(f"{self.instruction_prefix}LDA {self.symbol_table.get(operand)}")
                    self.instruction_prefix = "\t"
                if self.instructions[len(self.instructions) - 1].split()[0] == "STA":
                    del self.instructions[len(self.instructions) - 1]
                self.instructions.append(f"{self.instruction_prefix}STA {node.variable.variable.value}")

        if isinstance(node, IfStatementNode):
            self.__generate(node.condition)
            first_statement = True
            for stmt in node.body:
                if first_statement:
                    self.instruction_prefix = f"LABEL_{self.label_count} "
                    first_statement = False
                self.__generate(stmt)
            first_statement = True

            self.instruction_prefix = f"EXIT_{self.exit_label_count} "
            self.label_count += 1
            self.exit_label_count += 1

    def print_instructions(self):
        for x in self.instructions:
            print(x)

        for x in self.constant_instructions:
            print(x)

        for x in self.variable_instructions:
            print(x)

    def write_instruction_to_file(self, file):
        for x in self.instructions:
            file.write(x + "\n")

        for x in self.constant_instructions:
            file.write(x + "\n")

        for x in self.variable_instructions:
            file.write(x + "\n")
