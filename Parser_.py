from Nodes import *
from Tokens import *

class Parser:
    def __init__(self, tokens, ignore_no_tokens = False) -> None:
        self.tokens = iter(tokens)
        self.ignore_no_tokens = ignore_no_tokens
        self.advance()

    def parse(self):
        if (self.current_token == None and not self.ignore_no_tokens):
            self.raise_error("No tokens !")

        res = None
        res_a = []

        while self.can_advance():
            res = self.expr()
            #if isinstance(res, ReturnNode):
                #return RootNode(res_a + [res.return_value])
            res_a.append(res)

        return RootNode(res_a)

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def raise_error(self, e):
        raise Exception(f"[PARSER ERROR] {e}")

    def optional(self, t):
        if self.current_token == None:
            return False
        else:
            self.advance()
            if self.current_token.type == t:
                return True
            else:
                return False
                
    def eat(self, t):

        if self.current_token == None:
            self.raise_error(f"{t} was expected !")

        if self.current_token.type == t:
            value = self.current_token.value
            self.advance()
            return value
        else:
            self.raise_error(f"{t} was expected !")

    def factor(self):
        token = self.current_token

        if token == None:
            self.raise_error("Invalid Syntax !")

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            self.eat(TokenType.RPAREN)

            return result

        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)

        elif token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)

        elif token.type == TokenType.FALSE:
            self.advance()
            return FalseNode()

        elif token.type == TokenType.TRUE:
            self.advance()
            return TrueNode()

        elif token.type == TokenType.PLUS:
            self.advance()
            return PositiviteNumberNode(self.factor())

        elif token.type == TokenType.MINUS:
            self.advance()
            return NegativeNumberNode(self.factor())

        elif token.type == TokenType.IDENTIFIER:
            self.advance()

            if self.can_advance():
                if self.current_token.type == TokenType.LPAREN:
                    return CallFuncNode(token.value, self.parse_args())

                elif self.current_token.type == TokenType.EQUAL:
                    self.advance()
                    return SetVarNode(token.value, self.expr())

                #DEPRECATED
                """
                elif self.current_token.type == TokenType.DOT:
                    self.advance()
                    func_name = self.eat(TokenType.IDENTIFIER)
                    return CallClassFuncNode(token.value, func_name, self.parse_args())
                """

            return GetVarNode(token.value)

        elif token.type == TokenType.RETURN:
            self.advance()
            return ReturnNode(self.expr())

        elif token.type == TokenType.BREAK:
            self.advance()
            return BreakNode()

        elif token.type == TokenType.FUNC_DEF:
            self.advance()

            func_name = self.eat(TokenType.IDENTIFIER)
            func_args = self.parse_args()
            func_blocks = []

            while self.current_token.type != TokenType.END:
                e = self.expr()
                func_blocks.append(e)

            self.advance()
            return CustomFunctionNode(func_name, func_args, func_blocks)

        elif token.type == TokenType.NEW:
            self.advance()
            class_name = self.eat(TokenType.IDENTIFIER)
            args = self.parse_args()

            return InstanciateClassNode(class_name, args)

        elif token.type == TokenType.IF:
            self.advance()
            initial_condition = self.expr()

            self.eat(TokenType.THEN)
            
            #Conditional Node
            #COND | [OK] | [ELSE IF] | [ELSE]
            b_ok = []
            b_else_if = []
            b_else = []

            while self.current_token.type != TokenType.END:
                while self.current_token.type != TokenType.ELSE:
                    if self.current_token.type == TokenType.END:
                        break

                    b_ok.append(self.expr())

                if self.current_token.type == TokenType.ELSE:
                    self.advance()

                    if self.current_token.type == TokenType.IF:
                        self.advance()
                        cond = self.expr()
                        actual_else_if = []
                        self.optional(TokenType.THEN)

                        while self.current_token.type != TokenType.ELSE:
                            if self.current_token.type == TokenType.END:
                                break
                            actual_else_if.append(self.expr())

                        b_else_if.append(ElseIfNode(cond, actual_else_if))

                    else:
                        while self.current_token.type != TokenType.END:
                            b_else.append(self.expr())

            self.advance()
            return ConditionalNode(initial_condition, b_ok, b_else_if, b_else)

        elif token.type == TokenType.FOR:
            self.advance()
            
            identifier_name = self.eat(TokenType.IDENTIFIER)
            
            self.eat(TokenType.EQUAL)
            start = self.expr()

            self.eat(TokenType.COMMA)
            end = self.expr()

            blocks = []

            while self.current_token.type != TokenType.END:
                blocks.append(self.expr())

            self.eat(TokenType.END)

            return ForNode(identifier_name, start, end, blocks)

        elif token.type == TokenType.WHILE:
            self.advance()
            self.eat(TokenType.THAN)
            
            cond = self.expr()

            self.eat(TokenType.THEN)

            blocks = []

            while self.current_token.type != TokenType.END:
                blocks.append(self.expr())

            self.eat(TokenType.END)

            return WhileNode(cond, blocks)

        elif token.type == TokenType.NOT:
            self.advance()
            return NotNode(self.expr())

        elif token.type == TokenType.LBRACKET:
            content = self.parse_args(start_token = TokenType.LBRACKET, end_token = TokenType.RBRACKET)
            return ListNode(content)

        self.raise_error("NUMBER | PLUS | MINUS was expected !")

    def parse_args(self, start_token = TokenType.LPAREN, end_token = TokenType.RPAREN):
        self.eat(start_token)
        args = []

        if self.can_advance():
            if self.current_token.type != end_token:
                while self.can_advance():

                    e = self.expr()

                    if not self.can_advance(): break

                    if self.current_token.type in (TokenType.COMMA, end_token):
                        args.append(e)
                        
                        tok_type = self.current_token.type

                        if tok_type == end_token:
                            break
                        elif tok_type == TokenType.COMMA:
                            self.advance()

        self.eat(end_token)
        
        return args

    def term(self):
        result = self.factor()

        while self.can_advance() and self.current_token.type in (
            TokenType.TIMES,
            TokenType.DIVIDE,

            TokenType.LBRACKET,

            TokenType.DOT,

            TokenType.PLUS_PLUS,
            TokenType.MINUS_MINUS,
            TokenType.PLUS_EQ,
            TokenType.MINUS_EQ,
            TokenType.TIMES_EQ,
            TokenType.DIV_EQ,
            
            TokenType.EQEQ,
            TokenType.NEQ,
            TokenType.GTHAN,
            TokenType.GEQTHAN,
            TokenType.LTHAN,
            TokenType.LEQTHAN
        ):
                
            if self.current_token.type == TokenType.TIMES:
                self.advance()
                result = TimesNode(result, self.factor())

            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.factor())

            elif self.current_token.type == TokenType.LBRACKET:
                self.advance()
                a = self.factor()
                self.eat(TokenType.RBRACKET)
                need_equal = True
                
                if self.current_token != None:
                    if self.current_token.type == TokenType.EQUAL:
                        self.advance()
                        #I DONT KNOW OMG !! expr() or factor() ??? WHAT IS THE BEST
                        #b = self.factor() 
                        b = self.expr()
                        result = BracketSetNode(result, a, b)
                        need_equal = False

                if need_equal == True:
                    result = BracketGetNode(result, a)

            elif self.current_token.type == TokenType.DOT:
                self.advance()
                a = self.factor()
                result = DotAccessor(result, a)

            elif self.current_token.type == TokenType.PLUS_PLUS:
                self.advance()
                result = PlusPlusMinusMinusEtc(result, TokenType.PLUS_PLUS)

            elif self.current_token.type == TokenType.MINUS_MINUS:
                self.advance()
                result = PlusPlusMinusMinusEtc(result, TokenType.MINUS_MINUS)

            elif self.current_token.type == TokenType.PLUS_EQ:
                self.advance()
                result = PlusPlusMinusMinusEtc(result, TokenType.PLUS_EQ, self.factor())

            elif self.current_token.type == TokenType.MINUS_EQ:
                self.advance()
                result = PlusPlusMinusMinusEtc(result, TokenType.MINUS_EQ, self.factor())

            elif self.current_token.type == TokenType.TIMES_EQ:
                self.advance()
                result = PlusPlusMinusMinusEtc(result, TokenType.TIMES_EQ, self.factor())

            elif self.current_token.type == TokenType.DIV_EQ:
                self.advance()
                result = PlusPlusMinusMinusEtc(result, TokenType.DIV_EQ, self.factor())

            #Conditions
            elif self.current_token.type == TokenType.EQEQ:
                self.advance()
                result = EqEqNode(result, self.factor())

            elif self.current_token.type == TokenType.NEQ:
                self.advance()
                result = NotEqNode(result, self.factor())

            elif self.current_token.type == TokenType.GTHAN:
                self.advance()
                result = GThanNode(result, self.factor())

            elif self.current_token.type == TokenType.GEQTHAN:
                self.advance()
                result = GEqThanNode(result, self.factor())

            elif self.current_token.type == TokenType.LTHAN:
                self.advance()
                result = LThanNode(result, self.factor())

            elif self.current_token.type == TokenType.LEQTHAN:
                self.advance()
                result = LEqThanNode(result, self.factor())

        return result

    def expr(self):
        result = self.term()

        while self.can_advance() and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS
        ):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())

            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = MinusNode(result, self.term())

        while self.can_advance() and self.current_token.type in (
            TokenType.AND,
            TokenType.OR
        ):
            #Conditions
            if self.current_token.type == TokenType.AND:
                self.advance()
                result = AndNode(result, self.term())

            elif self.current_token.type == TokenType.OR:
                self.advance()
                a = result
                result = OrNode(result, self.term())
                
        return result

    def can_advance(self):
        return self.current_token != None