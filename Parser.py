from Nodes import *
from Token import TokenKind


class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token: Token = token_list[0]
        self.position = 0

    def advance(self):
        self.position += 1
        if self.position < len(self.token_list):
            self.current_token: Token = self.token_list[self.position]

    def parse(self):
        return self.expression()

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
