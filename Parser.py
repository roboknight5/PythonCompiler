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
    def look_ahead(self,offset=1)->Token:
        if self.position+offset<len(self.token_list):
            return self.token_list[self.position+offset]

    def parse(self):
        return self.statement_list()

    def statement_list(self):
        statement_list = []
        while True:
            if self.current_token.kind == TokenKind.EndOfFileToken:
                break
            expression = self.statement()
            print(self.current_token)
            if self.current_token.kind != TokenKind.SemicolonToken:
                raise Exception("Error missing semicolon")
            self.advance()
            statement_list.append(expression)
        return statement_list

    def declare_statement(self):
        if self.current_token.kind == TokenKind.IdentifierToken:
            variable = self.current_token
            self.advance()
            if self.current_token.kind == TokenKind.EqualToken:
                self.advance()
                for i in SymbolTable.symbol_table:
                    if i.variable.value == variable.value:
                        raise Exception(f"Variable {variable.value} is already declared")

                value = self.expression()
                var_node = VariableNode(variable=variable, value=value)
                SymbolTable.symbol_table.append(var_node)
                return var_node
        return AssignNode

    def assign_statement(self):
        if self.current_token.kind == TokenKind.IdentifierToken:
            variable = self.current_token
            self.advance()
            if self.current_token.kind == TokenKind.EqualToken:
                self.advance()

                value = self.expression()
                var_node = VariableNode(variable=variable, value=value)
                
                return var_node

    def statement(self):
        if self.current_token.kind == TokenKind.IntKeywordToken:
            self.advance()
            return self.declare_statement()

        if self.current_token.kind==TokenKind.IdentifierToken and self.look_ahead().kind==TokenKind.EqualToken:
            return self.assign_statement()




        expression = self.expression()
        return expression

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
            variable_value = None
            for var in SymbolTable.symbol_table:
                if var.variable.value == token.value:
                    variable_value = var.value
            if variable_value is None:
                raise Exception(f"Error unknown variable {token.value}")
            return VariableNode(token, variable_value)

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
