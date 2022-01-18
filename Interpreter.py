class Interpreter:
    def __init__(self, root_node, ctx) -> None:
        self.root_node = root_node
        self.root_node.context = ctx
        self.root_node.context.root_node = self.root_node
        
    def interpret(self):
        #A FAIRE : RETURN ICI
        #PAS DE ROOT_NODE, UNE ARRAY DE CHAQUE EXPR
        #for e in expr:
        #   if e == "return": break
        # ^ un truc comme ça ^
        return self.root_node.execute()