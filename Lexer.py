from Token import *


class Lexer:
    def __init__(self, text: str):
        self.input = text
        self.position = 0

    def current_char(self):
        if self.position >= len(self.input):
            return '\0'
        return self.input[self.position]

    def next(self):
        self.position += 1

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

        if self.current_char().isalpha():
            start = self.position
            while self.current_char().isalpha() or self.current_char().isdigit():
                self.next()
            length = self.position - start
            text = self.input[start:start + length]
            if text == "int":
                return Token(text, TokenKind.IntegerKeywordToken)
            return Token(text, TokenKind.IdentifierToken)

        if self.current_char().isspace():
            start = self.position
            while self.current_char().isspace():
                self.next()
            length = self.position - start
            text = self.input[start:length + start]
            return Token(text, TokenKind.WhiteSpaceToken)

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
            self.next()
            return Token("=", TokenKind.EqualToken)

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
