from Nodes import bool_to_node

screen = None

import pygame
pygame.mixer.init()

LOADED_IMAGES = {}

def chargerImage(path):
    img = pygame.image.load(path)
    id_ = len(LOADED_IMAGES)
    LOADED_IMAGES[id_] = img.convert()
    return id_

def changerTaille(id_, x, y):
    LOADED_IMAGES[id_] = pygame.transform.scale(LOADED_IMAGES[id_], (x, y))

def joueSon(path):
    s = pygame.mixer.Sound(path)
    s.play()

class Cercle:
    def __init__(self) -> None:
        self.color = (255, 255, 255)
        self.radius = 10

class Jeu:
    def __init__(self, title, sx, sy) -> None:
        global screen
        title = title.execute()
        sx = sx.execute()
        sy = sy.execute()
        pygame.init()
        screen = pygame.display.set_mode([sx, sy])
        pygame.display.set_caption(title)
        self.running = True

    def translate(self, k):
        if k == "gauche": return pygame.K_LEFT
        elif k == "droite": return pygame.K_RIGHT
        elif k == "haut": return pygame.K_UP
        elif k == "bas": return pygame.K_DOWN
        elif k == "espace": return pygame.K_SPACE

    def appuit(self, k):
        keys = pygame.key.get_pressed()
        return keys[self.translate(k)]

    def active(self):
        return self.running

    def remplir(self, r, g, b):
        try:
            screen.fill((r, g, b))
        except: pass

    def gerer(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def afficher(self):
        pygame.display.flip()

    def dessine(self, r, x, y):
        if isinstance(r, Cercle):
            pygame.draw.circle(
                screen,
                r.color,
                (x, y),
                r.radius
            )
        else:
            screen.blit(LOADED_IMAGES[r], (x, y))

    def __repr__(self) -> str:
        return "<Game Window>"