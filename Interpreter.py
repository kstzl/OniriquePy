class Interpreter:
    def __init__(self, root_node, ctx) -> None:
        self.root_node = root_node
        self.root_node.context = ctx
        self.root_node.context.root_node = self.root_node
        
    def interpret(self):
        return self.root_node.execute()