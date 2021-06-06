from Nodes import *


class CodeOptimizer:

    def optimize(self, stmt_list):
        stmt_list = self.__optimize_if(stmt_list)

        stmt_list = self.__optimize_operand(stmt_list)

        return stmt_list

    def __optimize_operand(self, stmt_list):
        for idx, var in enumerate(stmt_list):
            if isinstance(var, BinaryOpNode) or isinstance(var, UnaryOpNode) or isinstance(var, VariableNode) \
                    or isinstance(var, NumberNode):
                del stmt_list[idx]
        return stmt_list

    def __optimize_if(self, stmt_list):
        for idx, var in enumerate(stmt_list):
            if isinstance(var, IfStatementNode):
                stmt_list[idx].body = self.optimize(var.body)
                if not stmt_list[idx].body:
                    del stmt_list[idx]
        return stmt_list
