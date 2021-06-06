from Token import *


class Lexer:
    def __init__(self, text: str):
        self.input = text
        self.position = 0

    def current_char(self):
        if self.position >= len(self.input):
            return '\0'
        return self.input[self.position]

    def peek_ahead(self):
        if self.position + 1 >= len(self.input):
            return '\0'
        return self.input[self.position + 1]

    def next(self, offset=0):
        self.position += 1 + offset

    def next_token(self) -> Token:
        if self.position >= len(self.input):
            return Token("\0", TokenKind.EndOfFileToken)

        if self.current_char().isdigit():
            start = self.position
            while self.current_char().isdigit():
                self.next()
            length = self.position - start
            text = self.input[start:start + length]
            return Token(text, TokenKind.NumberToken)

        if self.current_char().isspace():
            start = self.position
            while self.current_char().isspace():
                self.next()
            length = self.position - start
            text = self.input[start:length + start]
            return Token(text, TokenKind.WhiteSpaceToken)

        if self.current_char().isalpha():
            start = self.position
            while self.current_char().isalpha() or self.current_char().isdigit() or self.current_char() == "_":
                self.next()
            length = self.position - start
            text = self.input[start:length + start]
            if text == "int":
                return Token(text, TokenKind.IntKeywordToken)
            if text == "if":
                return Token(text, TokenKind.IfKeywordToken)
            if text == "then":
                return Token(text, TokenKind.ThenKeywordToken)
            if text == "end":
                return Token(text, TokenKind.EndKeywordToken)
            return Token(text, TokenKind.IdentifierToken)

        if self.current_char() == "+":
            self.next()
            return Token("+", TokenKind.PlusToken)
        elif self.current_char() == "-":
            self.next()
            return Token("-", TokenKind.MinusToken)
        elif self.current_char() == "*":
            self.next()
            return Token("*", TokenKind.AsteriskToken)
        elif self.current_char() == "/":
            self.next()
            return Token("/", TokenKind.SlashToken)
        elif self.current_char() == "(":
            self.next()
            return Token("(", TokenKind.LeftParenthesisToken)
        elif self.current_char() == ")":
            self.next()
            return Token(")", TokenKind.RightParenthesisToken)
        elif self.current_char() == ";":
            self.next()
            return Token(";", TokenKind.SemicolonToken)
        elif self.current_char() == "=":
            if self.peek_ahead() == "=":
                self.next(1)
                return Token("==", TokenKind.EqualEqualToken)
            else:
                self.next()
                return Token("=", TokenKind.EqualToken)
        elif self.current_char() == ">":
            self.next()
            return Token(">", TokenKind.GreaterThanToken)
        elif self.current_char() == "<":
            self.next()
            return Token("<", TokenKind.SmallerThanToken)
        return Token("", TokenKind.BadToken)

    def lex(self):
        token_list = []
        while True:
            token = self.next_token()
            if token.kind == TokenKind.EndOfFileToken:
                token_list.append(token)
                break
            if token.kind == TokenKind.BadToken:
                raise Exception("Error Invalid Token")
            if token.kind != TokenKind.WhiteSpaceToken:
                token_list.append(token)

        for x in token_list:
            print(x)

        return token_list
