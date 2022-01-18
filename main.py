from math import sqrt, sin, cos, tan
from Context import Context
from Parser_ import Parser
from Tokenizer import *
from Tokens import *
from Nodes import *
from Interpreter import *
from OniPyGame import *

def _test():
    return 1

class Pomme:
    def __init__(self, couleur) -> None:
        self.couleur = couleur

    def changeCouleur(self, new_color):
        self.couleur = new_color

    def getColor(self):
        return self.couleur
        
    def afficheCouleur(self):
        print(f"Ma couleur : {self.couleur}")

    def __repr__(self) -> str:
        return "SUPER POMME"

tokenizer = Tokenizer("""
affiche("Salut, le monde !")

si 1 < 3 alors
    affiche("1 est inférieur à 3 !")
sinon si 2 == 3
    affiche("2 == 3!")
sinon
    affiche("Sinon ...")
fin

test = 100

affiche(test + 1)

tant que test < 110 alors
    affiche(test)
    test = test + 1
fin

pour i = 0, 5
    si i == 3 alors
        casse
    fin
    affiche(i)
fin

fonction ajoute(a, b)
    retourne a + b
fin

affiche(ajoute(1, 5))
""")

ctx = Context()
ctx.variables["x"]      = 13
ctx.variables["y"]      = True

ctx.classes["Pomme"]    = Pomme
ctx.classes["Jeu"]      = Jeu
ctx.classes["Cercle"]   = Cercle

ctx.functions["chargerImage"]   =   chargerImage
ctx.functions["changerTaille"]  =   changerTaille
ctx.functions["joueSon"]        =   joueSon

ctx.functions["sqrt"]   = lambda x: sqrt(x)
ctx.functions["sin"]    = lambda x: sin(x)
ctx.functions["cos"]    = lambda x: cos(x)
ctx.functions["tan"]    = lambda x: tan(x)
ctx.functions["add"]    = lambda x, y: x + y
ctx.functions["affiche"]  = lambda x: print(x)
ctx.functions["demande"]  = lambda x: input(x)
ctx.functions["test"]   = _test

tokens = tokenizer.generate_tokens()
root_node = Parser(tokens).parse()

i = Interpreter(root_node, ctx)
#root_node.context = ctx
#result = root_node.execute()

print(i.interpret())