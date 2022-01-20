class Context:
    def __init__(self) -> None:
        self.variables      = {}
        self.classes        = {}

        self.root_node      = None
        self.for_node       = None
        
    def check_variable(self, variable_name):
        if not variable_name in self.variables:
            raise Exception(f"[CONTEXT] La variable '{variable_name}' n'existe pas !")
            
    def check_class(self, class_name):
        if not class_name in self.classes:
            raise Exception(f"[CONTEXT] La classe '{class_name}' n'existe pas !")