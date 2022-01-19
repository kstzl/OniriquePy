from enum import Enum

class TokenType(Enum):
    NUMBER      =   0
    PLUS        =   1
    MINUS       =   2
    TIMES       =   3
    DIVIDE      =   4
    LPAREN      =   5
    RPAREN      =   6
    IDENTIFIER  =   7
    COMMA       =   8
    EQUAL       =   9
    RETURN      =   10
    FUNC_DEF    =   11
    END         =   12
    NEW         =   13
    DOT         =   14
    STRING      =   15

    EQEQ        =   16
    NEQ         =   17
    GTHAN       =   18
    GEQTHAN     =   19
    LTHAN       =   20
    LEQTHAN     =   21

    TRUE        =   22
    FALSE       =   23

    IF          =   24
    THEN        =   25
    ELSE        =   26
    ENDIF       =   27

    FOR         =   28
    BREAK       =   29

    WHILE       =   30
    THAN        =   31

    LBRACKET    =   32
    RBRACKET    =   33

    NOT         =   34

    PLUS_PLUS   =   35
    MINUS_MINUS =   36
    PLUS_EQ     =   37
    MINUS_EQ    =   38
    TIMES_EQ    =   39
    DIV_EQ      =   40

    AND         =   41
    OR          =   42

    POWER       =   43
    EACH        =   44
    IN          =   45

class Token:
    def __init__(self, t, v = None) -> None:
        self.type   = t
        self.value  = v

    def __repr__(self) -> str:
        return f"[{self.type} : {self.value}]"
