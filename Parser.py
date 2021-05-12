from Nodes import *
from Token import TokenKind


class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token: Token = token_list[0]
        self.position = 0

    def advance(self, offset=0):
        self.position += 1 + offset
        if self.position < len(self.token_list):
            self.current_token: Token = self.token_list[self.position]

    def peek(self, offset=0):
        return self.token_list[self.position + offset]

    def parse(self):
        return self.statement_list()

    def declare_statement(self):
        if self.current_token.kind == TokenKind.IdentifierToken:
            var_name = self.current_token
            self.advance()
            if self.current_token.kind == TokenKind.EqualToken:
                self.advance()
                value = self.expression()
                var_node = VarNode(var_name, value)
                for node in SymbolTable.sym_table:
                    if node.variable.value == var_name.value:
                        raise Exception(f"Variable {node.variable.value} is already Declared")

                SymbolTable.sym_table.append(var_node)
                return var_node
        else:
            raise Exception("Identifier required after keyword \'int\'")

    def assign_statement(self):
        var_name = self.current_token
        self.advance(1)
        value = self.expression()
        var_node = None
        for idx, var in enumerate(SymbolTable.sym_table):
            if var.variable.value == var_name.value:
                SymbolTable.sym_table[idx] = VarNode(var_name, value)
                var_node = VarNode(var_name, value)

        if var_node is None:
            raise Exception("Unknown identifier ")
        return var_node

    def statement(self):
        if self.current_token.kind == TokenKind.IntegerKeywordToken:
            self.advance()
            return self.declare_statement()

        if self.current_token.kind == TokenKind.IdentifierToken and self.peek(1).kind == TokenKind.EqualToken:
            return self.assign_statement()

        result = self.expression()
        return result

    def statement_list(self):
        stmt_list = []
        while self.current_token.kind != TokenKind.EndOfFileToken:
            result = self.statement()
            print(self.current_token)
            if self.current_token.kind != TokenKind.SemicolonToken:
                raise Exception("Error Missing Semicolon")
            self.advance()
            stmt_list.append(result)
        return stmt_list

    def expression(self):
        left = self.term()
        while self.current_token.kind == TokenKind.PlusToken or self.current_token.kind == TokenKind.MinusToken:
            operator_token = self.current_token
            self.advance()
            right = self.term()
            left = BinaryOpNode(left, operator_token, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token.kind == TokenKind.AsteriskToken or self.current_token.kind == TokenKind.SlashToken:
            operator_token = self.current_token
            self.advance()
            right = self.factor()
            left = BinaryOpNode(left, operator_token, right)
        return left

    def factor(self):
        token: Token = self.current_token
        if token.kind == TokenKind.NumberToken:
            self.advance()
            return NumberNode(token)
        if token.kind == TokenKind.IdentifierToken:
            self.advance()
            var_node = None
            for var in SymbolTable.sym_table:
                if var.variable.value == token.value:
                    var_node = var

            if var_node is None:
                raise Exception("Error Unknown identifier")
            return var_node

        if token.kind == TokenKind.PlusToken or token.kind == TokenKind.MinusToken:
            self.advance()
            factor = self.factor()
            return UnaryOpNode(operator=token, node=factor)
        if token.kind == TokenKind.LeftParenthesisToken:
            self.advance()
            expr = self.expression()
            if self.current_token.kind == TokenKind.RightParenthesisToken:
                self.advance()
                return expr
