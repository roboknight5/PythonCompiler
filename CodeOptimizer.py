from Nodes import *


class CodeOptimizer:

    def optimize(self, stmt_list):

        stmt_list = self.__optimize_operand(stmt_list)

        stmt_list=self.__optimize_if(stmt_list)

        return stmt_list

    def __optimize_operand(self, stmt_list):
        list=[]
        for idx, var in enumerate(stmt_list):
            if not isinstance(var,BinaryOpNode) and not isinstance(var,UnaryOpNode) and not isinstance(var,VariableNode) and not isinstance(var,NumberNode):
                list.append(var)
        return list

    def __optimize_if(self, stmt_list):
        list = []
        invalid_if=False
        for idx, var in enumerate(stmt_list):
            if isinstance(var, IfStatementNode):
                stmt_list[idx].body = self.optimize(var.body)
                if not  stmt_list[idx].body:
                    invalid_if=True
            if not invalid_if:
                list.append(var)

        return list