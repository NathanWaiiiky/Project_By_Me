"""import"""

from Bowser import*

""" la fenetre """
fen_width = 1200
fen_height = 720
fen = pygame.display.set_mode((fen_width, fen_height))
"""la varible de la taille de la grille """
taille_grille =40
class World():
    """
    met sur la map 2D tout les element qu'il y'a dans la grille
    """
    def __init__(self, data):
        global un_Goomba
        """
        :param Num_grille:
        """
        self.tile_list = []
        row_count = 0
        """____________________________les block de base__________________________________"""
        """ j'initilise l'image Herbe"""
        Herbe = pygame.image.load('Image/Bloc_Terre.png')
        """ j'initilise l'image brick"""
        Brick = pygame.image.load('Image/Bloc_Brique.png')
        """__je parcours la grille de jeux__ """
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    """je pose les block de brick sur la map"""
                    img_Brick = pygame.transform.scale(Brick, (taille_grille, taille_grille))
                    img_rect_Brick = img_Brick.get_rect()
                    img_rect_Brick.x = col_count * taille_grille
                    img_rect_Brick.y = row_count * taille_grille
                    tile_brick = (img_Brick, img_rect_Brick)
                    self.tile_list.append(tile_brick)
                if tile == 2:
                    """je pose les block d'herbe sur la map"""
                    img_herbe = pygame.transform.scale(Herbe, (taille_grille, taille_grille))
                    img_rect_herbe = img_herbe.get_rect()
                    img_rect_herbe.x = col_count * taille_grille
                    img_rect_herbe.y = row_count * taille_grille
                    tile_herbe = (img_herbe, img_rect_herbe)
                    self.tile_list.append(tile_herbe)
                if tile == 3:
                    """je pose la lave sur la map"""
                    Lave_entity = lave(col_count * taille_grille, row_count * taille_grille)
                    Lave_group.add(Lave_entity)
                if tile == 4:
                    """je pose le mob sur la map"""
                    Goomba_entity = Goomba(col_count * taille_grille, row_count * taille_grille)
                    Goomba_group.add(Goomba_entity)
                if tile == 9:
                    """je pose la porte final sur la map"""
                    Porte_entity =Porte(col_count * taille_grille, row_count * taille_grille)
                    Porte_group.add(Porte_entity)
                col_count += 1
            row_count += 1
    """dessine les block"""
    def draw(self):
        for tile in self.tile_list:
            fen.blit(tile[0], tile[1])

"""timer plant"""
add_14_sec = time.time() + 14
"""une plante toute les 14 sec"""
def plant_spwan(Lvl):
    global add_14_sec
    if Lvl==6:
        lvl_dificulte = 7
    else:
        lvl_dificulte = 14
    if time.time() > add_14_sec:
        i = r.randint(1, 2)
        if i == 1:
            Plante_feux_group.add(plante_de_feux())
        if i == 2:
            Plante_glace_group.add(plante_de_glace())
        add_14_sec = time.time() + lvl_dificulte
        return add_14_sec
