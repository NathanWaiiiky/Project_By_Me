"""import"""
import pygame
import time
import random as r
""" la fenetre """
fen_width = 1200
fen_height = 720
fen = pygame.display.set_mode((fen_width, fen_height))
"""level de la map"""
level_Map= 0
"""________________________________________________________________________joueur_____________________________________________________________________________________"""

class player():
    def __init__(self, x, y, World):
        """load toute les image d'animation + variable d'animation"""
        self.images_right = []
        self.images_left = []
        self.images_jump_right = pygame.image.load('Image/MARIO_Jump.png')
        self.images_jump_left = pygame.transform.flip(self.images_jump_right, True, False)
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'Image/MARIO_{num}.png')
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        """position et velocité du joueur """
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        """initialisation des son de mario"""
        self.jump_sound = pygame.mixer.Sound('Son/Mario_Jump.mp3')
        self.jump_sound.set_volume(0.1)
        self.dead_sound = pygame.mixer.Sound('Son/Mario_death.mp3')
        self.dead_sound.set_volume(0.1)
        self.upgrade_sound = pygame.mixer.Sound('Son/Mario_upgrade.mp3')
        self.upgrade_sound.set_volume(0.1)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = 1
        self.Ice_Power = False
        self.Fire_Power = False
        self.one_shot = time.time()
        self.time_pouvoir = time.time()
        """recolte les donnée du monde"""
        self.world = World
    """savoir ou est le joueur """
    def getX(self):
        """
        :return X:
        """
        return self.rect.x
    def getY(self):
        """
        :return Y:
        """
        return self.rect.y

    """quelle lvl de map?"""
    def get_lvl_map(self):
        """
        :return lvl_map:
        """
        global level_Map
        return level_Map
    def set_lvl_map(self,real_lvl):
        """
        :set lvl_map:
        """
        global level_Map
        level_Map = real_lvl
    """get du monde"""
    def Get_World(self):
        return self.world
    """get / set du temp du pouvoir"""
    def set_pouvoir(self,time):
        self.time_pouvoir = time
    def get_pouvoir(self):
        if self.time_pouvoir -time.time() >0:
            return self.time_pouvoir
        else:
            return time.time()
    """_____________________Permet l'animation de mario et son update _____________________________"""
    def update(self, game_over,World, BF_group, Fusee_grp,Bowser_Grp):
        global level_Map
        """actualiser le world"""
        self.world = World
        """variable ajustement moovement"""
        dx = 0
        dy = 0
        walk_cooldown = 5
        """ si il est pas mort"""
        if  game_over <=2:
            key = pygame.key.get_pressed()
            """touche gauche droite"""
            if key[pygame.K_LEFT]:
                dx -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.direction = 1
                self.counter += 1
            """boule de feux et de glace + timming 1  tire toute les 1 sec"""
            if key[pygame.K_b] and  time.time() >self.one_shot:
                if self.Ice_Power:
                    if self.direction == 1:
                        if self.jumped:
                            Boule_de_glace_group.add(boule_de_glace(self.rect.x + 40, self.rect.y + 2, self.direction))
                        else:
                            Boule_de_glace_group.add(boule_de_glace(self.rect.x + 35, self.rect.y + 45, self.direction))
                    else:
                        if self.jumped:
                            Boule_de_glace_group.add(boule_de_glace(self.rect.x + 0, self.rect.y + 2, self.direction))
                        else:
                            Boule_de_glace_group.add(boule_de_glace(self.rect.x + 0, self.rect.y + 45, self.direction))
                    self.one_shot = time.time() + 2
                if self.Fire_Power:
                    if self.direction == 1:
                        if self.jumped:
                            Boule_de_feu_group.add(boule_de_feu(self.rect.x + 40, self.rect.y + 2, self.direction))
                        else:
                            Boule_de_feu_group.add(boule_de_feu(self.rect.x + 35, self.rect.y + 45, self.direction))
                    else:
                        if self.jumped:
                            Boule_de_feu_group.add(boule_de_feu(self.rect.x + 0, self.rect.y + 2, self.direction))
                        else:
                            Boule_de_feu_group.add(boule_de_feu(self.rect.x + 0, self.rect.y + 45, self.direction))
                    self.one_shot = time.time() + 2
            """deguisement"""
            if self.Ice_Power:
                self.images_right = []
                self.images_left = []
                for num in range(1, 3):
                    img_right = pygame.image.load(f'Image/MARIO_ice_{num}.png')
                    img_left = pygame.transform.flip(img_right, True, False)
                    self.images_right.append(img_right)
                    self.images_left.append(img_left)
                self.image = self.images_right[self.index]
                self.images_jump_right = pygame.image.load('Image/MARIO_ice_Jump.png')
                self.images_jump_left = pygame.transform.flip(self.images_jump_right, True, False)

            if self.Fire_Power:
                self.images_right = []
                self.images_left = []
                for num in range(1, 3):
                    img_right = pygame.image.load(f'Image/MARIO_fire_{num}.png')
                    img_left = pygame.transform.flip(img_right, True, False)
                    self.images_right.append(img_right)
                    self.images_left.append(img_left)
                self.image = self.images_right[self.index]
                self.images_jump_right = pygame.image.load('Image/MARIO_fire_Jump.png')
                self.images_jump_left = pygame.transform.flip(self.images_jump_right, True, False)
            """temp du pouvoir"""
            if self.time_pouvoir < time.time():
                self.images_right = []
                self.images_left = []
                for num in range(1, 3):
                    img_right = pygame.image.load(f'Image/MARIO_{num}.png')
                    img_left = pygame.transform.flip(img_right, True, False)
                    self.images_right.append(img_right)
                    self.images_left.append(img_left)
                self.image = self.images_right[self.index]
                self.images_jump_right = pygame.image.load('Image/MARIO_jump.png')
                self.images_jump_left = pygame.transform.flip(self.images_jump_right, True, False)
                self.Ice_Power = False
                self.Fire_Power = False
            """touche Space"""
            if self.vel_y ==0:
                if key[pygame.K_SPACE] and self.jumped == False:
                    self.jump_sound.play()
                    self.vel_y = -15.7
                    self.jumped = True
                if key[pygame.K_SPACE] == False:
                    self.jumped = False
                if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                    self.counter = 0
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            """l'animation de mario qui bouge + saut"""
            if self.vel_y ==0:
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]
            else:
                if self.direction == 1:
                    self.image = self.images_jump_right
                if self.direction == -1:
                    self.image = self.images_jump_left
            """la gravité"""
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            """passer de level sauf pour le dernier lvl"""
            if level_Map != 7:
                if self.rect.x > 1200:
                    level_Map+=1
                    self.rect.x = 40
                    """colision contre le dernier niveaux"""
            elif self.rect.x >= 1180:
                dx = 0
                self.rect.x-=1
                """si il tombe"""
            if self.rect.y >700:
                game_over += 1
                self.rect.x = 40
                self.rect.y= 600
                self.dead_sound.play()
            """colision pour ne pas retourner au dernier niveaux"""
            if self.rect.x <= 10:
                dx = 0
                self.rect.x+=1
            """colision contre le haut du niveaux"""
            if self.rect.y <0:
                self.rect.y =+1
                dy = 0

            """parcourir les données du monde pour trouver ou il y'a une collision"""
            for tile in self.world.tile_list:

                """verif collision en X"""
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                """verif collision en X"""
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # verif si il saute
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # verif si il tombe
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
            """update la position du joueur """
            self.rect.x += dx
            self.rect.y += dy
            """colision entre sprite"""
            if pygame.sprite.spritecollide(self, Lave_group, False) :
                game_over +=1
                self.rect.x = 40
                self.rect.y = 600
                self.dead_sound.play()
            if pygame.sprite.spritecollide(self, Bowser_Grp, False) :
                game_over +=1
                self.rect.x = 40
                self.rect.y = 600
                self.dead_sound.play()
            if pygame.sprite.spritecollide(self, Goomba_group, False) :
                game_over += 1
                self.rect.x = 40
                self.rect.y = 600
                self.dead_sound.play()
            if pygame.sprite.spritecollide(self, BF_group, False) :
                game_over += 1
                self.rect.x = 40
                self.rect.y = 600
                self.dead_sound.play()
            if pygame.sprite.spritecollide(self, Fusee_grp, False) :
                game_over += 1
                self.rect.x = 40
                self.rect.y = 600
                self.dead_sound.play()
            if pygame.sprite.spritecollide(self, Porte_group, False) :
                level_Map = 1
                game_over =100
            if pygame.sprite.spritecollide(self, Plante_feux_group, False) and self.Ice_Power == False:
                self.Fire_Power = True
                self.time_pouvoir = time.time() + 10
                self.upgrade_sound.play()
            if pygame.sprite.spritecollide(self, Plante_glace_group, False) and self.Fire_Power == False:
                self.Ice_Power = True
                self.time_pouvoir = time.time() + 10
                self.upgrade_sound.play()
            """dessine le joueur"""
            fen.blit(self.image, self.rect)
            return game_over

"""________________________________________________________________________plant_feux_____________________________________________________________________________________"""

class plante_de_feux(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/Plant_Boule_de_feu.png')
        self.rect = self.image.get_rect()
        self.rect.x = r.randint(100,900)
        self.rect.y = 0
    def update(self):
        if self.rect.y <800:
            self.rect.y +=4

Plante_feux_group = pygame.sprite.Group()

"""________________________________________________________________________plant_glace_____________________________________________________________________________________"""

class plante_de_glace(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/Plant_de_glace.png')
        self.rect = self.image.get_rect()
        self.rect.x = r.randint(100, 900)
        self.rect.y = 0
    def update(self):
        if self.rect.y < 800:
            self.rect.y += 4

Plante_glace_group = pygame.sprite.Group()

"""________________________________________________________________________Boule de feux_____________________________________________________________________________________"""

class boule_de_feu(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image_ester_egg = pygame.image.load('Image/Boule_de_feu_easter_egg.png')
        self.image_real = pygame.image.load('Image/Boule_de_feu.png')
        self.image = self.image_real
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
    def update(self,lvl):
        if lvl == 4:
            self.image = self.image_ester_egg
        else:
            self.image = self.image_real
        if self.rect.y <800:
            if self.direction == 1:
                self.rect.x += 10
                self.rect.y += 2
            elif self.direction == -1:
                self.rect.x -=10
                self.rect.y +=2
        else:
            pass

Boule_de_feu_group = pygame.sprite.Group()

"""________________________________________________________________________Boule de glace_____________________________________________________________________________________"""

class boule_de_glace(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/Boule_de_glace.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
    def update(self):
        if self.rect.y <800:
            if self.direction == 1:
                self.rect.x += 10
                self.rect.y += 2
            elif self.direction == -1:
                self.rect.x -=10
                self.rect.y +=2
        else:
            pass


Boule_de_glace_group = pygame.sprite.Group()

"""________________________________________________________________________Goomba_____________________________________________________________________________________"""

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global level_Map
        pygame.sprite.Sprite.__init__(self)
        self.image_ester_egg= pygame.image.load('Image/Mob_Goomba_easter_egg.png')
        self.image_real =pygame.image.load('Image/Mob_Goomba.png')
        self.image= self.image_real
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 8
        self.initx = x
        self.moove = 1
        self.lvl = level_Map
        self.death_anime = False
        self.death_time = time.time()
        self.ice_time = time.time()
        self.ice = False
    def update(self,x_player,y_player,level_Map):

        if level_Map == 4:
            self.image = self.image_ester_egg
        else:
            self.image = self.image_real
        """saut sur la tete"""
        if y_player <= self.rect.y+10 and y_player >=self.rect.y- 15 :
            if x_player+20 >=self.rect.x  and x_player+20 <= self.rect.x+48 or x_player+10 >=self.rect.x  and x_player+10 <= self.rect.x+48 or x_player+30 >=self.rect.x  and x_player+30 <= self.rect.x+48:
                Goomba_ecrasee_entity = Goomba_ecrasee(self.rect.x, self.rect.y)
                Goomba_ecrasee_group.add(Goomba_ecrasee_entity)
                self.rect.y += 1000
        """bon lvl et animation"""
        if self.lvl == level_Map:
            if self.death_anime == False and self.ice == False:
                if self.rect.x >= self.initx + 42:
                    self.moove= -1
                if self.rect.x <= self.initx - 42:
                    self.moove= 1
                if self.moove ==-1:
                    self.rect.x -=1
                else:
                    self.rect.x +=1
            else:
                pass
        else:
            self.rect.y +=1000
        """mort par boule de feu ou glace"""
        if pygame.sprite.spritecollide(self, Boule_de_feu_group, False) and self.death_anime == False:
            self.death_anime= True
            self.death_time = time.time()+1
        if self.death_anime:
            self.image = pygame.image.load('Image/Mob_Goomba_dmg.png')
            if time.time() > self.death_time:
                self.rect.y += 1000
        if pygame.sprite.spritecollide(self, Boule_de_glace_group, False):
            self.ice = True
            self.ice_time = time.time() + 3
        if self.ice:
            self.image = pygame.image.load('Image/Mob_Goomba_Ice.png')
            if time.time() > self.ice_time:
                self.image =pygame.image.load('Image/Mob_Goomba.png')
                self.ice = False
"""goomba ecrasée"""
class Goomba_ecrasee(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global level_Map
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/Mob_écrasée.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lvl = level_Map
        self.time_anime = time.time()+0.1
    def update(self):
        if not self.lvl == level_Map:
            self.rect.y += 1000
        if self.time_anime < time.time():
            self.rect.y = 1000

"""Goomba"""
Goomba_group = pygame.sprite.Group()
"""goomba_ecrasée"""
Goomba_ecrasee_group = pygame.sprite.Group()
"""________________________________________________________________________lave_____________________________________________________________________________________"""

class lave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global level_Map
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/Lave.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lvl = level_Map
    def update(self):
        global level_Map
        if self.lvl == level_Map:
            pass
        else:
            self.rect.y = 1000

Lave_group = pygame.sprite.Group()

"""________________________________________________________________________porte_____________________________________________________________________________________"""
class Porte(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/Porte.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
Porte_group = pygame.sprite.Group()
