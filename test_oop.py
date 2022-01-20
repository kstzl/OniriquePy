from Nodes import *

class Test:
    def __init__(self):
        print("Test Initied")
        self.counter = NumberNode(1)
        self.prenom = StringNode("Rien")

    def lol(self):
        print("Lol ! xD")

    def setPrenom(self, prenom):
        self.prenom = prenom

    def affichePrenom(self):
        print("Prénom :", self.prenom.__print__())
        return self.prenom

    def __plus_plus__(self):
        self.counter += 1
        return NumberNode(self.counter)

    def __minus_minus__(self):
        self.counter -= 1
        return NumberNode(self.counter)