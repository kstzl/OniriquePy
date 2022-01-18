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

fenetre = nouveau Jeu("Flappy Bird", 800, 600)
perso = nouveau Cercle()
img = chargerImage("flappy/bird.png")

x = 800 / 2
y = 600 / 2

vely = 1
peutSauter = Vrai
perdu = Faux
c = 255

tant que fenetre.active() alors

    fenetre.gerer()

    si perdu == Faux alors

        fenetre.remplir(0, 0, 0)

        si fenetre.appuit("espace") alors
            si peutSauter alors
                peutSauter = Faux
                vely = -1
                joueSon("flappy/sfx_wing.wav")
            fin
        sinon
            peutSauter = Vrai
        fin
        
        changerTaille(img, 85, 85)
        fenetre.dessine(img, x, y)

        vely = vely + 0.001
        y = y + vely / 5

        si y > 750 alors
            perdu = Vrai
            joueSon("flappy/sfx_hit.wav")
            joueSon("flappy/sfx_die.wav")
        fin

    sinon
        fenetre.remplir(c, 0, 0)
        c = c - 0.25
    fin

    fenetre.afficher()
    
fin

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