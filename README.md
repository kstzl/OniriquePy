# OniriquePy
Petit test d'un langage de programmation en FRANCAIS !

ATTENTION : LE LANGAGE N'EST PAS PARFAIT ! C'EST SOURTOUT POUR M'ENTRAINER / TESTER DES TRUCS
          : A L'AVENIR JE PENSE FAIRE CE LANGAGE DANS UN LANGAGE COMPILÉ.

Example:
```python
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
```

Nous donne :
```
Salut, le monde !
1 est inférieur à 3 !
101.0
0
1
2
6.0
None
```
(None est la valeur de retour de la root_node)
