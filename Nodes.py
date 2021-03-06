from Interpreter import *
from Tokenizer import *
from Tokens import *
import Parser_
from Context import Context
import copy

def bool_to_node(b):
    return TrueNode() if b else FalseNode()

def node_to_bool(b):
    try:
        return b.__is_bool__()
    except:
        pass
    return False

class BaseNode:
    def __init__(self) -> None:
        pass

    def expect_node_type(self , s, node, expected_node_type):
        if not isinstance(node, expected_node_type):
            self.raise_error(f"Attention ! Tu as essayer {s} un {type(self)} avec {type(node)} ! \n Tu aurais du utiliser un {expected_node_type}.")

    def expect_index(self, actual, target):
        if actual > target:
            self.raise_error(f"Attention ! Tu essayes d'accéder à l'index {actual} sauf que la taille de la chaine de caractère n'est que de {target}")

    def raise_error(self, e):
        raise Exception(f"[NODE ERROR] {e}")

    def f_execute(self, other):
        self.context = other.context
        return self.execute()

    def __repr__(self) -> str:
        return "(Base Node)"


class BracketGetNode(BaseNode):
    def __init__(self, node, index) -> None:
        self.node = node
        self.index = index

    def execute(self):
        node_executed = self.node.f_execute(self)
        id_executed = self.index.f_execute(self)
        return node_executed.__bracket_get__(id_executed)

    def __repr__(self) -> str:
        return f"(GET[{self.index}] from {self.node})"

class BracketSetNode(BaseNode):
    def __init__(self, node, index, val) -> None:
        self.node = node
        self.index = index
        self.val = val

    def execute(self):
        node_executed = self.node.f_execute(self)
        id_executed = self.index.f_execute(self)
        val_executed = self.val.f_execute(self)
        return node_executed.__bracket_set__(id_executed, val_executed)

    def __repr__(self) -> str:
        return f"({self.node}[{self.index}] = {self.val})"

class RootNode(BaseNode):
    def __init__(self, nodes) -> None:
        self.nodes = nodes
        self.context = {}
        self.returned = None

    def stop_return(self, res):
        self.returned = res

    def execute(self):
        res = None
        for node in self.nodes:
            res = node.f_execute(self)
            if self.returned != None: 
                res = self.returned
                break

        return res

    def __repr__(self) -> str:
        return "(Root Node)"

class StringNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value
        self.taille = NumberNode(len(self.value))

    def __bracket_get__(self, other):
        self.expect_node_type("de recupérer un index dans un", other, NumberNode)
        i = int(other.execute().value)
        self.expect_index(i, len(self.value) - 1)
        return StringNode(self.value[i])

    def __bracket_set__(self, index, val):
        self.expect_node_type("de mettre un index dans un", index, NumberNode)
        i = int(index.execute().value)
        self.expect_index(i, len(self.value) - 1)
        to_list = list(self.value)
        to_list[i] = val.execute().value
        return StringNode("".join(to_list))

    def __func_call__(self, args):
        self.context.check_variable(self.value)
        v = self.context.variables[self.value]
        if v != None:
            if isinstance(v, BaseNode):
                return v.__func_call__(args)
            return v(*args)
        else:
            self.raise_error(f"Vous avez essayé d'appeler la chaine '{self.value}' mais la fonction associé n'existe pas.")

    def __iterate__(self):
        return [StringNode(e) for e in self.value]

    def __eqeq__(self, other):
        self.expect_node_type("==", other, StringNode)
        return bool_to_node(self.value == other.execute().value)

    def __neq__(self, other):
        self.expect_node_type("!=", other, StringNode)
        return bool_to_node(self.value != other.execute().value)

    def __subbed__(self, other):
        self.expect_node_type("-", other, NumberNode)
        return StringNode(self.value[:-int(other.execute().value)])

    def __added__(self, other):
        #self.expect_node_type("+", other, StringNode)
        #return StringNode(self.value + other.execute().value)
        return StringNode(self.value + other.execute().__print__())

    def __plus_eq__(self, other):
        self.expect_node_type("+", other, StringNode)
        return StringNode(self.value + other.execute().value)

    def __minus_minus__(self):
        return StringNode(self.value[:-1])

    def __minus_eq__(self, other):
        self.expect_node_type("-=", other, NumberNode)
        return StringNode(self.value[:-int(other.execute().value)])

    def __multed__(self, factor):
        self.expect_node_type("string * value", factor, NumberNode)
        f = factor.f_execute(self).value
        return StringNode(self.value * int(f))

    def __print__(self):
        return self.value

    def __size__(self):
        return NumberNode(len(self.value))

    def __number__(self):
        return NumberNode(int(self.value))

    def execute(self):
        return self

    def enMajuscule(self):
        return StringNode(self.value.upper())

    def enMinuscule(self):
        return StringNode(self.value.lower())

    def separe(self, separator):
        self.expect_node_type("séparer", separator, StringNode)
        to_list = self.value.split(separator.value)
        res = [StringNode(e) for e in to_list]
        return ListNode(res)

    def __repr__(self) -> str:
        return f"(\"{self.value}\")"

class NumberNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value

    def __is_bool__(self):
        return True if self.value > 0 else None

    def __not__(self):
        return 0 if self.value > 0 else 1

    def __powed__(self, other):
        self.expect_node_type("d'ajouter", other, NumberNode)
        return NumberNode(self.value ** other.execute().value)

    def __added__(self, other):
        self.expect_node_type("d'ajouter", other, NumberNode)
        return NumberNode(self.value + other.execute().value)

    def __subbed__(self, other):
        self.expect_node_type("de soustraire", other, NumberNode)
        return NumberNode(self.value - other.execute().value)

    def __multed__(self, other):
        self.expect_node_type("de multiplier", other, NumberNode)
        return NumberNode(self.value * other.execute().value)

    def __divided__(self, other):
        self.expect_node_type("de diviser", other, NumberNode)
        right = other.execute().value
        if right == 0:
            self.raise_error(f"Attention ! Tu as voulu diviser {self.value} par {right} !")
        return NumberNode(self.value / right)

    def __eqeq__(self, other):
        self.expect_node_type("==", other, NumberNode)
        right = other.execute().value
        return bool_to_node(self.value == right)

    def __neq__(self, other):
        self.expect_node_type("!=", other, NumberNode)
        right = other.execute().value
        return bool_to_node(self.value != right)

    def __gthan__(self, other):
        self.expect_node_type(">", other, NumberNode)
        right = other.execute().value
        return bool_to_node(self.value > right)

    def __geqthan__(self, other):
        self.expect_node_type(">=", other, NumberNode)
        right = other.execute().value
        return bool_to_node(self.value >= right)

    def __lthan__(self, other):
        self.expect_node_type("<", other, NumberNode)
        right = other.execute().value
        return bool_to_node(self.value < right)

    def __leqthan__(self, other):
        self.expect_node_type("<=", other, NumberNode)
        right = other.execute().value
        return bool_to_node(self.value <= right)

    def __plus_plus__(self):
        return NumberNode(self.value + 1)

    def __minus_minus__(self):
        return NumberNode(self.value - 1)

    def __plus_eq__(self, other):
        self.expect_node_type("+=", other, NumberNode)
        return NumberNode(self.value + other.execute().value)

    def __minus_eq__(self, other):
        self.expect_node_type("-=", other, NumberNode)
        return NumberNode(self.value - other.execute().value)

    def __times_eq__(self, other):
        self.expect_node_type("*=", other, NumberNode)
        return NumberNode(self.value * other.execute().value)

    def __div_eq__(self, other):
        self.expect_node_type("/=", other, NumberNode)
        b = other.execute().value
        if b == 0:
            self.raise_error(f"Attention ! Tu as voulu diviser {self.value} par {b} !")
        return NumberNode(self.value / b)

    def __print__(self):
        return str(self.value)

    def execute(self):
        return self

    def __repr__(self) -> str:
        return f"({self.value})"

class TrueNode(BaseNode):
    def __init__(self) -> None:
        pass

    def execute(self):
        return self
    
    def __is_bool__(self):
        return True

    def __not__(self):
        return FalseNode()

    def __repr__(self) -> str:
        return "(TRUE NODE)"

    def __print__(self):
        return "Vrai"

class FalseNode(BaseNode):
    def __init__(self) -> None:
        pass

    def execute(self):
        return self

    def __is_bool__(self):
        return False

    def __not__(self):
        return TrueNode()

    def __repr__(self) -> str:
        return "(FALSE NODE)"

    def __print__(self):
        return "Faux"

class NullNode(BaseNode):
    def __init__(self) -> None:
        pass

    def execute(self):
        return self

    def __is_bool__(self):
        return False

    def __not__(self):
        return TrueNode()

    def __repr__(self) -> str:
        return "(NULL NODE)"

    def __print__(self):
        return "Rien"

class PositiviteNumberNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value
        
    def execute(self):
        return NumberNode(+self.value.f_execute(self).value)

    def __repr__(self) -> str:
        return f"+{self.value}"

class NegativeNumberNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value
        
    def execute(self):
        return NumberNode(-self.value.f_execute(self).value)

    def __repr__(self) -> str:
        return f"-{self.value}"

class PowerNode(BaseNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__powed__(right)

class AddNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__added__(right)

    def __repr__(self) -> str:
        return f"({self.left} + {self.right})"

class MinusNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__subbed__(right)
        #return self.left.f_execute(self) - self.right.f_execute(self)

    def __repr__(self) -> str:
        return f"({self.left} - {self.right})"

class TimesNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__multed__(right)

    def __repr__(self) -> str:
        return f"({self.left} * {self.right})"

class DivideNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__divided__(right)

    def __repr__(self) -> str:
        return f"({self.left} / {self.right})"

class GetVarNode(BaseNode):
    def __init__(self, var_name) -> None:
        self.var_name = var_name
        
    def execute(self):
        self.context.check_variable(self.var_name)
        return self.context.variables[self.var_name]

    def __repr__(self) -> str:
        return f"(GET: {self.var_name})"

class SetVarNode(BaseNode):
    def __init__(self, var_name, var_content) -> None:
        self.var_name = var_name
        self.var_content = var_content

    def execute(self):
        res = self.var_content.f_execute(self)
        self.context.variables[self.var_name] = res
        return res

    def __repr__(self) -> str:
        return f"(SET: {self.var_name})"

class CallFuncNode(BaseNode):
    def __init__(self, func, args) -> None:
        self.func = func
        self.args = args

    def execute_args(self, custom_node = None):
        _executed_args = []
        #Executing all args:
        for arg in self.args:
            if custom_node != None:
                _executed_args.append(arg.f_execute(custom_node))
            else:
                _executed_args.append(arg.f_execute(self))
        return _executed_args

    def execute(self):
        #func = self.context.variables[self.func]
        res = self.func.f_execute(self)

        if isinstance(self.func, DotAccessor):
            r = res(*self.execute_args())
            return r

        else:
            r = self.func.__func_call__(self.args)
            return r

    def __repr__(self) -> str:
        return f"({self.func}())"

class ReturnNode(BaseNode):
    def __init__(self, return_value) -> None:
        self.return_value = return_value

    def execute(self):
        res = self.return_value.f_execute(self)
        self.context.root_node.stop_return(res)
        return res

    def __repr__(self) -> str:
        return "(return)"

class EndNode(BaseNode):
    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        return NullNode()
    
    def __repr__(self) -> str:
        return "(end)"

class CustomClassNode(BaseNode):
    def __init__(self, class_name, class_params, class_content):
        self.class_name = class_name
        self.class_params = class_params
        self.class_content = class_content

    def __func_call__(self, args):
    
        #Instanciated Object
        io = InstanciateClassNode(self.class_name, self.class_params)

        #Assigning Self
        self.context.variables["moi"] = io

        #Checking for the constructor
        for b in self.class_content:
            if isinstance(b, CustomFunctionNode):
                if b.func_name == self.class_name:
                    b.f_execute(self)
                    b.__func_call__(args)

            setattr(io, b.func_name, b)

        return io

    def execute(self):
        self.context.variables[self.class_name] = self
        return self

    def __repr__(self) -> str:
        return f"(class definition {self.class_name})"

class CustomFunctionNode(BaseNode):
    def __init__(self, func_name, func_params, func_content) -> None:
        self.func_name      = func_name
        self.func_params    = func_params
        self.func_content   = func_content

    def __func_call__(self, args):
        #Setting  context
        ctx = copy.deepcopy(self.context)

        #Checking parameters
        if len(args) > len(self.func_params):
            self.raise_error("Trop de paramètres !")

        elif len(args) < len(self.func_params):
            self.raise_error("Pas assez de paramètres")

        #Setting variables
        for i, _ in enumerate(self.func_params):
            param_name      = self.func_params[i].name
            param_result    = args[i]

            ctx.variables[param_name] = param_result

        #Creating an Interpreter instance !
        i = Interpreter(RootNode(self.func_content), ctx)

        #Return the value
        return i.interpret()

    def execute(self):
        self.context.variables[self.func_name] = self
        return self

    def __repr__(self) -> str:
        return f"(function definition {self.func_name})"

class InstanciateClassNode(BaseNode):
    def __init__(self, class_name, params) -> None:
        self.class_name = class_name
        self.params = params

    def execute(self):
        self.context.check_class(self.class_name)
        self.instance = self.context.classes[self.class_name](*self.params)
        return self.instance

    def __repr__(self) -> str:
        return f"(instance of {self.class_name})"
        
class CallClassFuncNode(BaseNode):
    def __init__(self, var_name, func_name, func_params) -> None:
        self.var_name = var_name
        self.func_name = func_name
        self.func_params = func_params

    def execute(self):
        var = self.context.variables[self.var_name]
        func = getattr(var, self.func_name)

        executed_args = []

        #Executing all args:
        for param in self.func_params:
            executed_args.append(param.f_execute(self))

        return func(*executed_args)

    def __repr__(self) -> str:
        return f"Call Class Func Node"

class EqEqNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__eqeq__(right)

    def __repr__(self) -> str:
        return f"({self.left} == {self.right})"

class NotEqNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__neq__(right)

    def __repr__(self) -> str:
        return f"({self.left} != {self.right})"

class GThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__gthan__(right)

    def __repr__(self) -> str:
        return f"({self.left} > {self.right})"

class GEqThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__geqthan__(right)

    def __repr__(self) -> str:
        return f"({self.left} >= {self.right})"

class LThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__lthan__(right)

    def __repr__(self) -> str:
        return f"({self.left} < {self.right})"

class LEqThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        left = self.left.f_execute(self)
        right = self.right.f_execute(self)
        return left.__leqthan__(right)

    def __repr__(self) -> str:
        return f"({self.left} <= {self.right})"

class ElseIfNode(BaseNode):
    def __init__(self, condition, blocks) -> None:
        self.condition = condition
        self.blocks = blocks

    def execute(self):
        pass

    def __repr__(self) -> str:
        return f"(ElseIf : {self.condition})"

class ConditionalNode(BaseNode):
    def __init__(self, condition, blocks_ok, blocks_else_if, blocks_else) -> None:
        self.condition = condition
        self.blocks_ok = blocks_ok
        self.blocks_else_if = blocks_else_if
        self.blocks_else = blocks_else

    def execute(self):
        initial_condition = self.condition.f_execute(self)

        else_if_executed = False
        ret_val = None

        if node_to_bool(initial_condition):
            #I = Interpreter(RootNode(self.blocks_ok), self.context)
            #ret_val = I.interpret()
            for b in self.blocks_ok:
                b.f_execute(self)

        else:
            for else_if_block in self.blocks_else_if:
                cond = else_if_block.condition.f_execute(self)

                if node_to_bool(cond):
                    #I = Interpreter(RootNode(else_if_block.blocks), self.context)
                    #ret_val = I.interpret()
                    for b in else_if_block.blocks:
                        b.f_execute(self)

                    else_if_executed = True
                    break

            if not else_if_executed:
                #I = Interpreter(RootNode(self.blocks_else), self.context)
                #ret_val = I.interpret()
                for b in self.blocks_else:
                    b.f_execute(self)

        return NullNode()

    def __repr__(self) -> str:
        return f"(If : {self.condition})"

class BreakNode(BaseNode):
    def __init__(self) -> None:
        pass

    def execute(self):
        if self.context.loop_node == None:
            self.raise_error("The Break is not inside a for or while loop !")
        else:
            self.context.loop_node.broken = True

    def __repr__(self) -> str:
        return "(break)"

class ForNode(BaseNode):
    def __init__(self, identifier_name, start, end, blocks) -> None:
        self.identifier_name = identifier_name
        self.start = start
        self.end = end
        self.blocks = blocks

    def execute(self):
        
        self.broken = False

        start = int(self.start.f_execute(self).value)
        end = int(self.end.f_execute(self).value)
        
        if start > end:
            loop = reversed(range(end, start))
        else:
            loop = range(start, end)

        #self.context = copy.deepcopy(self.context)
        self.context.loop_node = self

        for i in loop:
            
            self.context.variables[self.identifier_name] = NumberNode(i)

            for b in self.blocks:
                if not self.broken:
                    b.f_execute(self)

    def __repr__(self) -> str:
        return f"(ForNode {self.identifier_name}={self.start} -> {self.end})"

class ForEachNode(BaseNode):
    def __init__(self, identifier_name, var, blocks):
        self.identifier_name = identifier_name
        self.var = var
        self.blocks = blocks

    def execute(self):

        self.broken = False

        #self.context = copy.deepcopy(self.context)
        self.context.loop_node = self

        var_iterator = self.var.f_execute(self).__iterate__()

        for element in var_iterator:
            self.context.variables[self.identifier_name] = element

            for b in self.blocks:
                if not self.broken:
                    b.f_execute(self)

    def __repr__(self):
        return f"(ForEach {self.identifier_name} IN {self.var})"

class WhileNode(BaseNode):
    def __init__(self, cond, blocks) -> None:
        self.cond = cond
        self.blocks = blocks

    def execute(self):

        self.broken = False
        
        #self.context = copy.deepcopy(self.context)
        self.context.loop_node = self

        while node_to_bool(self.cond.f_execute(self)) and not self.broken:
            for b in self.blocks:
                if not self.broken:
                    b.f_execute(self)

    def __repr__(self) -> str:
        return f"(While {self.cond})"

class NotNode(BaseNode):
    def __init__(self, node) -> None:
        self.node = node

    def execute(self):
        return self.node.f_execute(self).__not__()

    def __repr__(self) -> str:
        return f"(NOT{self.node}"

class DotAccessor(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right
        
    def execute(self):
        left = self.left.f_execute(self)
        right = self.right

        if hasattr(left, right.name):
            r = getattr(left, right.name)
            return r

        self.raise_error(f"Attention ! {left} ne peut pas fonctionner avec \"{right}\" !")

    def __repr__(self) -> str:
        return f"({self.left}.{self.right})"

class IdentifierNode(BaseNode):
    def __init__(self, name):
        self.name = name
        self.show_result = True

    def __equal__(self, n):
        n = n.f_execute(self)
        self.set_v(n)
        return n

    def __print__(self):
        return self.get_v()

    def itest(self, o):
        if isinstance(o, IdentifierNode):
            return o.get_v()
        else:
            return o

    #REDIRECTING THINGS LOOOOL
    def __added__(self, other):
        return self.get_v().__added__(self.itest(other))
    
    def __subbed__(self, other):
        return self.get_v().__subbed__(self.itest(other))

    def __multed__(self, other):
        return self.get_v().__multed__(self.itest(other))

    def __divided__(self, other):
        return self.get_v().__divided__(self.itest(other))

    def __eqeq__(self, other):
        return self.get_v().__eqeq__(self.itest(other))

    def __bracket_get__(self, index):
        return self.get_v().__bracket_get__(self.itest(index))

    def __bracket_set__(self, index, val):
        return self.set_v(self.get_v().__bracket_set__(self.itest(index), val))

    def __plus_plus__(self):
        return self.set_v(self.get_v().__plus_plus__())

    def __minus_minus__(self):
        return self.set_v(self.get_v().__minus_minus__())

    def __plus_eq__(self, other):
        return self.set_v(self.get_v().__plus_eq__(self.itest(other)))

    def __minus_eq__(self, other):
        return self.set_v(self.get_v().__minus_eq__(self.itest(other)))

    def __times_eq__(self, other):
        return self.set_v(self.get_v().__times_eq__(self.itest(other)))

    def __div_eq__(self, other):
        return self.set_v(self.get_v().__div_eq__(self.itest(other)))

    def __func_call__(self, args):
        a = [e.f_execute(self) for e in args]
        g = self.get_v()
        if isinstance(g, BaseNode):
            g.f_execute(self)
            return g.__func_call__(a)
        return self.context.variables[self.name](*a)

    def get_v(self):
        return self.context.variables[self.name]

    def set_v(self, v):
        self.context.variables[self.name] = v
        return v

    def execute(self):
        if not self.name in self.context.variables:
            self.set_v(NullNode())
        #self.context.variables[self.name] = NullNode()
        return self.get_v() if self.show_result else self

    def __repr__(self):
        return f"(Identifier: {self.name})"

class PlusPlusMinusMinusEtc(BaseNode):
    def __init__(self, node, tok, val = None):
        self.node = node
        self.tok = tok
        self.val = val

        self.node.show_result = False

    def execute(self):

        if self.val != None:
            r = self.val.f_execute(self)
            
        node = self.node.f_execute(self)
        result = None

        if self.tok == TokenType.EQUAL:

            if hasattr(node, "is_bracket"):
                s = node.bracket_set
                result = node.old_node.__bracket_set__(s, r)
            else:
                result = node.__equal__(r)

        elif self.tok == TokenType.PLUS_PLUS:
            result =  node.__plus_plus__()
        elif self.tok == TokenType.MINUS_MINUS:
            result = node.__minus_minus__()
        elif self.tok == TokenType.PLUS_EQ:
            result = node.__plus_eq__(self.val)
        elif self.tok == TokenType.MINUS_EQ:
            result =  node.__minus_eq__(self.val)
        elif self.tok == TokenType.TIMES_EQ:
            result = node.__times_eq__(self.val)
        elif self.tok == TokenType.DIV_EQ:
            result = node.__div_eq__(self.val)
        elif self.tok == TokenType.LBRACKET:
            result = node.__bracket_get__(self.val)
            result.is_bracket = True
            result.bracket_set = self.val
            result.old_node = node

        return result.f_execute(self)

    def __repr__(self):
        return f"({self.tok}{self.node})"

class AndNode(BaseNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self):
        a = self.left.f_execute(self)
        b = self.right.f_execute(self)
        r = bool_to_node(node_to_bool(a) and node_to_bool(b))
        return r

    def __repr__(self):
        return f"({self.left} AND {self.right})"
    
class OrNode(BaseNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self):
        a = self.left.f_execute(self)
        b = self.right.f_execute(self)
        r = bool_to_node(node_to_bool(a) or node_to_bool(b))
        return r

    def __repr__(self):
        return f"({self.left} OR {self.right})"

class ListNode(BaseNode):
    def __init__(self, content):
        self.content = content

    def execute(self):
        return self

    def ajoute(self, *other):
        for e in other:
            self.content.append(e)

    def supprime(self, indexes):
        for index in indexes:
            self.expect_node_type("de supprimer un index dans un", index, NumberNode)
            i = int(index.execute().value)
            self.expect_index(i, len(self.content) - 1)
            self.content.pop(i)
        return self.content

    def __iterate__(self):
        return [e for e in self.content]

    def __added__(self, other):
        if isinstance(other, ListNode):
            return ListNode(self.content + other.execute().content)
        else:
            self.content.append(other)
            return self

    def __minus_minus__(self):
        return ListNode(self.content[:-1])
            
    def __multed__(self, other):
        self.expect_node_type("de multiplier un tableau dans un", other, NumberNode)
        i = int(other.execute().value)
        return ListNode(self.content * i)

    def __plus_eq__(self, other):
        return self.__added__(other)

    def __times_eq__(self, other):
        return self.__multed__(other)

    def __size__(self):
        return NumberNode(len(self.content))

    def __bracket_get__(self, other):
        self.expect_node_type("de recupérer un index dans un", other, NumberNode)
        i = int(other.execute().value)
        self.expect_index(i, len(self.content) - 1)
        return self.content[i]

    def __bracket_set__(self, index, val):
        self.expect_node_type("de mettre un index dans un", index, NumberNode)
        i = int(index.execute().value)
        self.expect_index(i, len(self.content) - 1)
        self.content[i] = val.execute()
        return ListNode(self.content)

    def __repr__(self):
        return f"(Liste : {self.content})"

class ImportNode(BaseNode):
    def __init__(self, module_path):
        self.module_path = module_path

    def execute(self):
        v = self.module_path.f_execute(self).value
        try:
            f = open(v, encoding = "utf-8")

            tokens = Tokenizer(f.read()).generate_tokens()
            f.close()
            
            root_node = Parser_.Parser(tokens).parse()
            root_node.f_execute(self)
        except Exception as e:
            self.raise_error(f"Impossible d'importer le module {v} !")

    def __repr__(self):
        return f"(Import '{self.module_path}')"