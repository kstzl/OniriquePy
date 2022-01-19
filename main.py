from math import sqrt, sin, cos, tan
from Context import Context
from Parser_ import Parser
from Tokenizer import *
from Tokens import *
from Nodes import *
from Interpreter import *

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

tokenizer = Tokenizer("""
a = [
    "Kevin",
    "Nathan",
    "Tom",
    "Lucas",
    "Diego"
]

pour i = 0, taille(a)
    affiche(a[i])
fin
""")

ctx = Context()
ctx.variables["x"]              = NumberNode(10)
ctx.functions["sqrt"]           = lambda x: NumberNode(sqrt(x.execute().value))
ctx.functions["sin"]            = lambda x: NumberNode(sin(x.execute().value))
ctx.functions["cos"]            = lambda x: NumberNode(cos(x.execute().value))
ctx.functions["tan"]            = lambda x: NumberNode(tan(x.execute().value))
ctx.functions["affiche"]        = affiche
ctx.functions["demande"]        = demande
ctx.functions["taille"]         = taille

tokens = tokenizer.generate_tokens()
root_node = Parser(tokens).parse()

i = Interpreter(root_node, ctx)
print("Valeure de la root_node :", i.interpret())