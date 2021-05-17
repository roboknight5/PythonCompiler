from enum import Enum


class TokenKind(Enum):
    NumberToken = 0
    PlusToken = 1
    MinusToken = 2
    AsteriskToken = 3
    SlashToken = 4
    EndOfFileToken = 5
    BadToken = 6
    WhiteSpaceToken = 7
    LeftParenthesisToken = 8
    RightParenthesisToken = 9
    SemicolonToken = 10
    IdentifierToken = 11
    IntKeywordToken = 12
    EqualToken = 13



class Token:
    def __init__(self, value: str, kind: TokenKind):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return "Kind: " + self.kind.name + " Value: " + self.value
