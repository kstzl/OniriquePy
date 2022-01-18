from mimetypes import init
from Interpreter import *
from Context import Context
import copy

def bool_to_node(b):
    return TrueNode() if b else FalseNode()

def node_to_bool(b):
    return True if isinstance(b, TrueNode) or b == 1 else False

class BaseNode:
    def __init__(self) -> None:
        pass

    def raise_error(self, e):
        raise Exception(f"[NODE ERROR] {e}")

    def f_execute(self, other):
        self.context = other.context
        return self.execute()

    def __repr__(self) -> str:
        return "Base Node"

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
        return "Root Node"

class StringNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value

    def execute(self):
        return self.value

    def __repr__(self) -> str:
        return f"STRING : {self.value}"

class NumberNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value

    def execute(self):
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"

class TrueNode(BaseNode):
    def __init__(self) -> None:
        pass

    def execute(self):
        return 1

    def __repr__(self) -> str:
        return "Vrai"

class FalseNode(BaseNode):
    def __init__(self) -> None:
        pass

    def execute(self):
        return 0

    def __repr__(self) -> str:
        return "Faux"

class PositiviteNumberNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value
        
    def execute(self):
        return +self.value.f_execute(self)

    def __repr__(self) -> str:
        return f"+{self.value}"

class NegativeNumberNode(BaseNode):
    def __init__(self, value) -> None:
        self.value = value
        
    def execute(self):
        return -self.value.f_execute(self)

    def __repr__(self) -> str:
        return f"-{self.value}"

class AddNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return self.left.f_execute(self) + self.right.f_execute(self)

    def __repr__(self) -> str:
        return f"({self.left} + {self.right})"

class MinusNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return self.left.f_execute(self) - self.right.f_execute(self)

    def __repr__(self) -> str:
        return f"({self.left} - {self.right})"

class TimesNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return self.left.f_execute(self) * self.right.f_execute(self)

    def __repr__(self) -> str:
        return f"({self.left} * {self.right})"

class DivideNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        a = self.left.f_execute(self)
        b = self.right.f_execute(self)
        if b == 0: self.raise_error(f"Division By Zero ! ({a} / {b})")
        return a / b

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
    def __init__(self, func_name, args) -> None:
        self.func_name = func_name
        self.args = args

    def execute(self):
        self.context.check_function(self.func_name)

        executed_args = []

        #Executing all args:
        for arg in self.args:
            executed_args.append(arg.f_execute(self))

        func = self.context.functions[self.func_name]
        is_custom = isinstance(func, CustomFunctionNode)

        if is_custom:
            #parser = Parser_.Parser(func.func_content, ignore_no_tokens = True)
            #root_node = parser.parse()

            ctx = copy.deepcopy(self.context)

            #Setting variables - CHECK
            if len(executed_args) > len(func.func_params):
                self.raise_error("Too much parameters !")

            elif len(executed_args) < len(func.func_params):
                self.raise_error("Missing parameters !")

            #Setting variables
            for i, _ in enumerate(func.func_params):
                param_name      = func.func_params[i].var_name
                param_result    = executed_args[i]

                ctx.variables[param_name] = param_result

            i = Interpreter(RootNode(func.func_content), ctx)

            return i.interpret()

        else:
            return func(*executed_args)

    def __repr__(self) -> str:
        return f"{self.func_name}"

class ReturnNode(BaseNode):
    def __init__(self, return_value) -> None:
        self.return_value = return_value

    def execute(self):
        res = self.return_value.f_execute(self)
        self.context.root_node.stop_return(res)
        return res

    def __repr__(self) -> str:
        return "Return"

class EndNode(BaseNode):
    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        return None
    
    def __repr__(self) -> str:
        return "End Node"

class CustomFunctionNode(BaseNode):
    def __init__(self, func_name, func_params, func_content) -> None:
        self.func_name      = func_name
        self.func_params    = func_params
        self.func_content   = func_content

    def execute(self):
        self.context.functions[self.func_name] = self

    def __repr__(self) -> str:
        return "Custom Function Definition"

class InstanciateClassNode(BaseNode):
    def __init__(self, class_name, params) -> None:
        self.class_name = class_name
        self.params = params

    def execute(self):
        self.context.check_class(self.class_name)
        self.instance = self.context.classes[self.class_name](*self.params)
        return self.instance

    def __repr__(self) -> str:
        return f"INSTANCE OF {self.class_name}"
        
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
        return bool_to_node(self.left.f_execute(self) == self.right.f_execute(self))

    def __repr__(self) -> str:
        return f"{self.left} == {self.right}"

class NotEqNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return bool_to_node(self.left.f_execute(self) != self.right.f_execute(self))

    def __repr__(self) -> str:
        return f"{self.left} != {self.right}"

class GThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return bool_to_node(self.left.f_execute(self) > self.right.f_execute(self))

    def __repr__(self) -> str:
        return f"{self.left} > {self.right}"

class GEqThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return bool_to_node(self.left.f_execute(self) >= self.right.f_execute(self))

    def __repr__(self) -> str:
        return f"{self.left} >= {self.right}"

class LThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return bool_to_node(self.left.f_execute(self) < self.right.f_execute(self))

    def __repr__(self) -> str:
        return f"{self.left} < {self.right}"

class LEqThanNode(BaseNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def execute(self):
        return bool_to_node(self.left.f_execute(self) <= self.right.f_execute(self))

    def __repr__(self) -> str:
        return f"{self.left} <= {self.right}"

class ElseIfNode(BaseNode):
    def __init__(self, condition, blocks) -> None:
        self.condition = condition
        self.blocks = blocks

    def execute(self):
        pass

    def __repr__(self) -> str:
        return f"ElseIfNode ({self.condition})"

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

        #return None

    def __repr__(self) -> str:
        return f"Conditional Node ({self.condition})"

class BreakNode(BaseNode):
    def __init__(self) -> None:
        pass

    def execute(self):
        if self.context.loop_node == None:
            self.raise_error("The Break is not inside a for or while loop !")
        else:
            self.context.loop_node.broken = True

    def __repr__(self) -> str:
        return "BREAK NODE !!!"

class ForNode(BaseNode):
    def __init__(self, identifier_name, start, end, blocks) -> None:
        self.identifier_name = identifier_name
        self.start = start
        self.end = end
        self.blocks = blocks
        self.broken = False

    def execute(self):
        
        start = int(self.start.f_execute(self))
        end = int(self.end.f_execute(self))
        
        if start > end:
            loop = reversed(range(end, start))
        else:
            loop = range(start, end)

        self.context = copy.deepcopy(self.context)
        self.context.loop_node = self

        for i in loop:
            
            self.context.variables[self.identifier_name] = i

            for b in self.blocks:
                if not self.broken:
                    b.f_execute(self)

    def __repr__(self) -> str:
        return f"ForNode ({self.identifier_name}={self.start} -> {self.end})"

class WhileNode(BaseNode):
    def __init__(self, cond, blocks) -> None:
        self.cond = cond
        self.blocks = blocks
        self.broken = False

    def execute(self):
        
        self.context = copy.deepcopy(self.context)
        self.context.loop_node = self

        while node_to_bool(self.cond.f_execute(self)) and not self.broken:
            for b in self.blocks:
                if not self.broken:
                    b.f_execute(self)

    def __repr__(self) -> str:
        return f"WHILE ({self.cond})"