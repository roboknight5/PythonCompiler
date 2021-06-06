from lxml.html.diff import token

from Nodes import *
from Token import TokenKind


class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token: Token = token_list[0]
        self.position = 0
        self.in_if_statement = False
        self.if_sym_table = []
        self.in_if_operand=False

    def advance(self, offset=0):
        self.position += 1 + offset
        if self.position < len(self.token_list):
            self.current_token: Token = self.token_list[self.position]

    def look_ahead(self, offset=1) -> Token:
        if self.position + offset < len(self.token_list):
            return self.token_list[self.position + offset]

    def look_behind(self, offset=1) -> Token:
        if self.position - offset < len(self.token_list):
            return self.token_list[self.position - offset]

    def parse(self):
        return self.statement_list()

    def statement_list(self):
        statement_list = []
        while True:
            if self.current_token.kind == TokenKind.EndOfFileToken:
                break
            if self.current_token.kind == TokenKind.EndKeywordToken and self.look_ahead().kind == TokenKind.SemicolonToken:
                self.advance()
                break
            if self.current_token.kind == TokenKind.EndKeywordToken and self.look_ahead().kind != TokenKind.SemicolonToken:
                raise Exception("Error missing semicolon")

            expression = self.statement()
            # print(self.current_token)
            # tok_list={TokenKind.LeftParenthesisToken,TokenKind.RightParenthesisToken,TokenKind.PlusToken,TokenKind.MinusToken,TokenKind.SlashToken,TokenKind.AsteriskToken,
            #           TokenKind.SmallerThanToken,TokenKind.GreaterThanToken,TokenKind.EqualEqualToken,TokenKind.EqualToken,TokenKind.NumberToken,TokenKind.IdentifierToken,TokenKind.}
            tok_list = [t.value for t in TokenKind]
            tok_list.remove(TokenKind.SemicolonToken)
            if self.current_token.kind in tok_list:
                raise Exception(f'unexpected token {self.current_token.value}')

            if self.current_token.kind != TokenKind.SemicolonToken:
                print('error ' + str(self.current_token))
                raise Exception("Error missing semicolon")

            self.advance()
            statement_list.append(expression)
        return statement_list

    def declare_statement(self):

        if self.in_if_statement:
            raise Exception("Can not have declaration inside if statement")

        self.advance()
        if self.current_token.kind == TokenKind.IdentifierToken:
            variable = self.current_token
            for i in SymbolTable.symbol_table:
                if i.variable.value == variable.value:
                    raise Exception(f"Variable {variable.value} is already declared")
            self.advance()
            if self.current_token.kind == TokenKind.EqualToken:
                self.advance()
                value = self.expression()
                if self.current_token.kind == TokenKind.EqualEqualToken or \
                        self.current_token.kind == TokenKind.GreaterThanToken or \
                        self.current_token.kind == TokenKind.SmallerThanToken:
                    raise Exception("Can not have logical operator in declaration  ")
                var_node = VariableNode(variable=variable, value=value)
                SymbolTable.symbol_table.append(var_node)
                return AssignNode(VariableNode(variable=variable, value=value))
            SymbolTable.symbol_table.append(VariableNode(variable, None))
            return AssignNode(VariableNode(variable=variable, value=None))

    def assign_statement(self):
        if self.current_token.kind == TokenKind.IdentifierToken:
            variable = self.current_token
            self.advance()
            if self.current_token.kind == TokenKind.EqualToken:
                table = []
                self.advance()
                if self.in_if_statement:
                    table = self.if_sym_table
                else:
                    table = SymbolTable.symbol_table

                value = self.expression()
                if self.current_token.kind == TokenKind.EqualEqualToken or \
                        self.current_token.kind == TokenKind.GreaterThanToken or \
                        self.current_token.kind == TokenKind.SmallerThanToken:
                    raise Exception("Can not have logical operator in assignment  ")

                var_node = VariableNode(variable=variable, value=value)
                for idx, var in enumerate(table):
                    if var.variable.value == variable.value:
                        table[idx] = VariableNode(variable, value)
                        var_node = VariableNode(variable, value)
                if var_node is None:
                    raise Exception("Unknown identifier ")
                return AssignNode(var_node)

    def if_statement(self):
        self.if_sym_table = SymbolTable.symbol_table.copy()
        if self.in_if_statement:
            raise Exception("can not have nested if statements")
        self.in_if_statement = True
        self.advance()
        expression = self.logical_expression()
        if self.current_token.kind != TokenKind.ThenKeywordToken:
            raise Exception("Error Missing 'then' after 'if' condition ")
        self.advance()

        statements = self.statement_list()
        self.in_if_statement = False
        return IfStatementNode(expression, statements)

    def statement(self):
        if self.current_token.kind == TokenKind.IntKeywordToken:
            return self.declare_statement()

        if self.current_token.kind == TokenKind.IdentifierToken and self.look_ahead().kind == TokenKind.EqualToken:
            return self.assign_statement()

        if self.current_token.kind == TokenKind.IfKeywordToken:
            return self.if_statement()

        expression = self.expression()
        if self.current_token.kind == TokenKind.EqualEqualToken or \
                self.current_token.kind == TokenKind.GreaterThanToken or \
                self.current_token.kind == TokenKind.SmallerThanToken:
            raise Exception("Can not have logical operator as an expression  ")

        return expression

    def logical_expression(self):
        self.in_if_operand=True
        left = self.expression()

        while self.current_token.kind == TokenKind.EqualEqualToken \
                or self.current_token.kind == TokenKind.GreaterThanToken \
                or self.current_token.kind == TokenKind.SmallerThanToken:
            operator_token = self.current_token
            self.advance()
            right = self.expression()
            left = BinaryOpNode(left, operator_token, right)
            return left
        raise Exception("If statement condition needs to contain '>' '==' '<'")

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
            # tok_list_after = [TokenKind.LeftParenthesisToken, TokenKind.RightParenthesisToken,TokenKind.PlusToken,TokenKind.AsteriskToken,
            #                   TokenKind.SlashToken,]
            # tok_list_after = [t.value for t in TokenKind]
            # tok_list_after.remove(TokenKind.SemicolonToken)
            tok_list_common = [TokenKind.PlusToken, TokenKind.MinusToken, TokenKind.AsteriskToken, TokenKind.SlashToken,
                               TokenKind.EqualToken, TokenKind.GreaterThanToken,
                               TokenKind.SmallerThanToken,TokenKind.EqualEqualToken]
            tok_list_after = [TokenKind.RightParenthesisToken, TokenKind.SemicolonToken, TokenKind.ThenKeywordToken]
            tok_list_behind = [TokenKind.EqualToken, TokenKind.LeftParenthesisToken, TokenKind.IfKeywordToken,TokenKind.SemicolonToken,TokenKind.EndOfFileToken,TokenKind.ThenKeywordToken]

            # Valid After
            if self.look_ahead().kind not in tok_list_after and \
                    self.look_ahead().kind not in tok_list_common:
                raise Exception(f"unexpected token '{self.look_ahead().value}' after {self.current_token.value}")
            if self.look_behind().kind not in tok_list_behind \
                    and self.look_behind().kind not in tok_list_common: raise Exception(
                f"unexpected token '{self.look_behind().value}' before {self.current_token.value} ")

            self.advance()
            return NumberNode(token)
        if token.kind == TokenKind.IdentifierToken:
            # tok_list_common = [TokenKind.PlusToken, TokenKind.MinusToken, TokenKind.AsteriskToken, TokenKind.SlashToken,
            #                    TokenKind.EqualToken, TokenKind.GreaterThanToken,
            #                    TokenKind.SmallerThanToken]
            # tok_list_after = [TokenKind.RightParenthesisToken, TokenKind.SemicolonToken]
            # tok_list_behind = [TokenKind.EqualToken, TokenKind.LeftParenthesisToken]
            tok_list_common = [TokenKind.PlusToken, TokenKind.MinusToken, TokenKind.AsteriskToken, TokenKind.SlashToken,
                               TokenKind.EqualToken, TokenKind.GreaterThanToken,
                               TokenKind.SmallerThanToken,TokenKind.EqualEqualToken]
            tok_list_after = [TokenKind.RightParenthesisToken, TokenKind.SemicolonToken, TokenKind.ThenKeywordToken]
            tok_list_behind = [TokenKind.EqualToken, TokenKind.LeftParenthesisToken, TokenKind.IfKeywordToken,
                               TokenKind.SemicolonToken, TokenKind.EndOfFileToken,TokenKind.ThenKeywordToken]

            # Valid After
            if self.look_ahead().kind not in tok_list_after and \
                    self.look_ahead().kind not in tok_list_common:
                raise Exception(f"unexpected token '{self.look_ahead().value}' after {self.current_token.value}")
            if self.look_behind().kind not in tok_list_behind \
                    and self.look_behind().kind not in tok_list_common: raise Exception(
                f"unexpected token '{self.look_behind().value}' before {self.current_token.value} ")
            self.advance()
            variable_value = None
            variable_name = None
            table = []
            if self.in_if_statement:
                table = self.if_sym_table
            else:
                table = SymbolTable.symbol_table

            for var in table:
                if var.variable.value == token.value:
                    variable_value = var.value
                    variable_name = var.variable.value

            if variable_name is None:
                raise Exception(f"Error unknown variable {token.value}")

            if variable_value is None:
                raise Exception(f"Error variable {token.value} has no value ")

            return VariableNode(token, variable_value)

        if token.kind == TokenKind.MinusToken:
            self.advance()
            factor = self.factor()
            return UnaryOpNode(operator=token, node=factor)
        if token.kind == TokenKind.PlusToken:
            raise Exception("Can't have '+' as unary operator ")
        if token.kind == TokenKind.SlashToken:
            raise Exception("Can't have '/' as unary operator ")
        if token.kind == TokenKind.AsteriskToken:
            raise Exception("Can't have '*' as unary operator ")

        if token.kind == TokenKind.RightParenthesisToken:
            raise Exception("unexpected token')'")
        if token.kind==TokenKind.EqualEqualToken :
            raise Exception("unexpected token '=='")
        if token.kind==TokenKind.GreaterThanToken :
            raise Exception("unexpected token '>'")
        if token.kind==TokenKind.SmallerThanToken :
            raise Exception("unexpected token '<'")



        if token.kind == TokenKind.LeftParenthesisToken:
            # tok_list_common = [TokenKind.LeftParenthesisToken, TokenKind.RightParenthesisToken]
            # tok_list_before=[TokenKind.IdentifierToken,TokenKind.NumberToken]
            # if self.look_ahead().kind in tok_list_common:raise Exception(f"unexpected token '{self.look_ahead().value}' ")
            # if self.look_behind().kind in tok_list_common and self.look_behind().kind in tok_list_before: raise Exception(f"unexpected token '{self.look_behind().value}' ")

            self.advance()

            expr = self.expression()
            if self.current_token.kind == TokenKind.RightParenthesisToken:
                self.advance()
                return expr
            else:
                txt=""
                if self.in_if_statement:
                    txt="and can't have Parenthesis surrounding logical expression"

                raise Exception("Missing ')' "+txt)
        if token.kind == TokenKind.SemicolonToken:
            raise Exception("unexpected token `;`")
