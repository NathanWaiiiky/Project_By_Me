"""import"""
from PlaceSprite import*
from math import *
"""__Le Menu__"""

"""__Les competences___"""
def truncate(n, decimals=0):
    r = floor(float(n)*10**decimals)/10**decimals
    return str(r)

"""Affichage"""
def Affiche(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    fen.blit(img, (x, y))

"""Bouton pour le menu"""
class Bouton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False
    def draw(self):
        Do = False
        """la position de la souris """
        posi = pygame.mouse.get_pos()
        """click + verif posi souris"""
        if self.rect.collidepoint(posi) and (pygame.mouse.get_pressed()[0] == 1 and self.click == False):
            Do = True
            self.click = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
        """draw le boutton"""
        fen.blit(self.image, self.rect)
        return Do