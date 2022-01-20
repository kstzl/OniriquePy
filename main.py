from math import sqrt, sin, cos, tan
from Context import Context
from Parser_ import Parser
from Tokenizer import *
from Tokens import *
from Nodes import *
from Interpreter import *
from test_oop import *

def affiche(*nodes):
    for node in nodes:
        try:
            print(node.__print__(), end = " ")
        except: print(node, end = " ")
    print("")

def demande(node):
    try:
        return StringNode(input(node.__print__()))
    except:
        return StringNode(input(node))

def taille(node):
    try:
        return node.__size__()
    except:
        return NumberNode(0)

def nombre(node):
    try:
        return node.__number__()
    except:
        return NumberNode(0)

tokenizer = Tokenizer("""
importe "test_module.oni"

q = nombre(demande("Combien de mdr voulez vous ? "))

si q == 0 alors
    affiche("Tu as mit zéro mdr ... Je suis déçu")
sinon
    affiche(mdr(q))
fin

""")

ctx = Context()
ctx.variables["x"]              = NumberNode(10)
ctx.variables["sqrt"]           = lambda x: NumberNode(sqrt(x.execute().value))
ctx.variables["sin"]            = lambda x: NumberNode(sin(x.execute().value))
ctx.variables["cos"]            = lambda x: NumberNode(cos(x.execute().value))
ctx.variables["tan"]            = lambda x: NumberNode(tan(x.execute().value))
ctx.variables["affiche"]        = affiche
ctx.variables["demande"]        = demande
ctx.variables["taille"]         = taille
ctx.variables["nombre"]         = nombre
ctx.classes["Test"]             = Test
ctx.variables["test"]           = lambda: print("called")

tokens = tokenizer.generate_tokens()
root_node = Parser(tokens).parse()

i = Interpreter(root_node, ctx)
print("Valeure de la root_node :", i.interpret())