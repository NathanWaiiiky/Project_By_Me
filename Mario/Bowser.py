"""import"""
import time

from Player_and_Sprite import*
"""______________________________________________________Bowser_______________________________________________________________________"""
"""les tps d'action"""
life = 10
tps_action_fusee = time.time()
tps_action_BF = time.time()
def get_tps_bf():
    global tps_action_BF
    if tps_action_BF - time.time() >0:
        return tps_action_BF
    else:
        return time.time()
def get_tps_Fusee():
    global tps_action_fusee
    if tps_action_fusee - time.time() >0:
        return tps_action_fusee
    else:
        return time.time()
def get_Life():
    global life
    return life

class Bowser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        """plusieur image"""
        self.List_image =[pygame.image.load('Image/Bowser.png'),pygame.image.load('Image/Bowser_Ice.png'),pygame.image.load('Image/Bowser_Dmg.png')]
        self.image = self.List_image[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temps_aspect = time.time()
        self.Boule_Traverse_corp = time.time()
        self.death_Bowser_sound = pygame.mixer.Sound('Son/Bowser_death.mp3')
        self.death_Bowser_sound.set_volume(0.1)
        self.dmg_Bowser_sound = pygame.mixer.Sound('Son/Bowser_Dmg.mp3')
        self.dmg_Bowser_sound.set_volume(0.1)
        self.feu_Bowser_sound = pygame.mixer.Sound('Son/Bowser_feu.mp3')
        self.feu_Bowser_sound.set_volume(0.1)
        self.fusee_Bowser_sound = pygame.mixer.Sound('Son/Bowser_fusee.mp3')
        self.fusee_Bowser_sound.set_volume(0.1)
        self.Win_sound = pygame.mixer.Sound('Son/Mario_end.mp3')
        self.Win_sound.set_volume(0.1)
        self.auto = False
    def update(self):
        global tps_action_fusee, tps_action_BF,life
        self.image = self.List_image[self.index]
        """temp de l'aspect"""
        if self.temps_aspect <time.time() and life > 0:
            self.index = 0
            key = pygame.key.get_pressed()

            if key[pygame.K_a] and time.time() > tps_action_BF:
                boule_de_feu_bowser_group.add(boule_feu_bowser(410, -100))
                boule_de_feu_bowser_group.add(boule_feu_bowser(730, -100))
                tps_action_BF = time.time()+10
                self.feu_Bowser_sound.play()
            if key[pygame.K_z] and time.time() > tps_action_fusee:
                Fusee_group.add(Fusee(1200, 160))
                Fusee_group.add(Fusee(1200, 400))
                tps_action_fusee = time.time() + 10
                self.fusee_Bowser_sound.play()
            if self.auto and time.time() - 3 > tps_action_BF:
                boule_de_feu_bowser_group.add(boule_feu_bowser(410, -100))
                boule_de_feu_bowser_group.add(boule_feu_bowser(730, -100))
                tps_action_BF = time.time() + 10
                self.feu_Bowser_sound.play()
            if self.auto and time.time() > tps_action_fusee:
                Fusee_group.add(Fusee(1200, 160))
                Fusee_group.add(Fusee(1200, 400))
                tps_action_fusee = time.time() + 10
                self.fusee_Bowser_sound.play()
            if key[pygame.K_m]:
                self.auto = True

        if pygame.sprite.spritecollide(self, Boule_de_feu_group, False) and self.Boule_Traverse_corp <time.time():
            self.index = 2
            self.temps_aspect = time.time()+0.3
            """si il meurt"""
            if life == 1:
                self.temps_aspect = time.time() + 2
                self.death_Bowser_sound.play()
            else:
                self.dmg_Bowser_sound.play()
            life -= 1
            self.Boule_Traverse_corp = time.time() + 1
        if pygame.sprite.spritecollide(self, Boule_de_glace_group, False):
            self.index = 1
            self.temps_aspect = time.time() + 4
        if life == 0 and self.temps_aspect <time.time():
            self.rect.y= 1000
            self.Win_sound.play()
Bowser_group = pygame.sprite.Group()
"""__________________________________________________Boule de feu____________________________________________________________________________"""
class boule_feu_bowser(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/boule_de_feu_bowser_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.y < 900:
            self.rect.y+=7


boule_de_feu_bowser_group = pygame.sprite.Group()
"""_____________________________________________________fusée__________________________________________________________________________"""
class Fusee(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/Fusee.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """evite lag"""
        if self.rect.x <1300:
            self.rect.x-=7


Fusee_group = pygame.sprite.Group()