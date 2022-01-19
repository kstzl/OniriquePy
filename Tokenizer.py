from Tokens import *

WHITESPACE = " \n\t"
DIGITS = "0123456789"


class Tokenizer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == "#":
                self.advance()
                while self.current_char != None:
                    if self.current_char == "\n": break
                    self.advance()

            elif self.current_char == "." or self.current_char in DIGITS:
                yield self.generate_number_or_dot()
            elif self.current_char.isalpha():
                yield self.generate_identifier()
            elif self.current_char == "+":
                self.advance()
                if self.current_char == "+":
                    self.advance()
                    yield Token(TokenType.PLUS_PLUS)
                elif self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.PLUS_EQ)
                else:
                    yield Token(TokenType.PLUS)
            elif self.current_char == "-":
                self.advance()
                if self.current_char == "-":
                    self.advance()
                    yield Token(TokenType.MINUS_MINUS)
                elif self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.MINUS_EQ)
                else:
                    yield Token(TokenType.MINUS)
            elif self.current_char == "*":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.TIMES_EQ)
                else:
                    yield Token(TokenType.TIMES)
            elif self.current_char == "/":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.DIV_EQ)
                else:
                    yield Token(TokenType.DIVIDE)
            elif self.current_char == "^":
                self.advance()
                yield Token(TokenType.POWER)
            elif self.current_char == "(":
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ")":
                self.advance()
                yield Token(TokenType.RPAREN)
            elif self.current_char == "[":
                self.advance()
                yield Token(TokenType.LBRACKET)
            elif self.current_char == "]":
                self.advance()
                yield Token(TokenType.RBRACKET)
            elif self.current_char == ",":
                self.advance()
                yield Token(TokenType.COMMA)
            elif self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.EQEQ)
                else:
                    yield Token(TokenType.EQUAL)
            elif self.current_char == "!":
                self.advance( )
                if self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.NEQ)
                else:
                    yield Token(TokenType.NOT)

            elif self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.GEQTHAN)
                else:
                    yield Token(TokenType.GTHAN)
            elif self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    yield Token(TokenType.LEQTHAN)
                else:
                    yield Token(TokenType.LTHAN)
            elif self.current_char == "\"":
                self.advance()
                yield self.generate_string()
            else:
                raise Exception(f'[TOKENIZER] Illegal character "{self.current_char}"')

    def generate_string(self):
        result = ""

        while self.current_char != None:
            if self.current_char == "\"": break
            result += self.current_char
            self.advance()

        self.advance()

        return Token(TokenType.STRING, result)

    def generate_identifier(self):
        result = ""

        while self.current_char != None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if result == "retourne":
            return Token(TokenType.RETURN)
        
        elif result == "fonction":
            return Token(TokenType.FUNC_DEF)

        elif result == "fin":
            return Token(TokenType.END)

        elif result == "nouveau" or result == "nouvelle":
            return Token(TokenType.NEW)

        elif result == "Faux":
            return Token(TokenType.FALSE)

        elif result == "Vrai":
            return Token(TokenType.TRUE)

        elif result == "si":
            return Token(TokenType.IF)

        elif result == "alors":
            return Token(TokenType.THEN)

        elif result == "sinon":
            return Token(TokenType.ELSE)

        elif result == "et":
            return Token(TokenType.AND)

        elif result == "ou":
            return Token(TokenType.OR)

        elif result == "chaque":
            return Token(TokenType.EACH)

        elif result == "dans":
            return Token(TokenType.IN)

        #DEPRECATED
        #elif result == "finif":
            #return Token(TokenType.ENDIF)

        elif result == "pour":
            return Token(TokenType.FOR)

        elif result == "casse":
            return Token(TokenType.BREAK)

        elif result == "tant":
            return Token(TokenType.WHILE)

        elif result == "que":
            return Token(TokenType.THAN)

            
        return Token(TokenType.IDENTIFIER, result)
        
    def generate_number_or_dot(self):
        decimal_point_count = 0
        number_str = self.current_char
        self.advance()

        while self.current_char != None and (self.current_char == "." or self.current_char in DIGITS):
            if self.current_char == ".":
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            number_str += self.current_char
            self.advance()

        if number_str == ".":
            return Token(TokenType.DOT)

        if number_str.startswith("."):
            number_str = "0" + number_str
        if number_str.endswith("."):
            number_str += "0"

        return Token(TokenType.NUMBER, float(number_str))
