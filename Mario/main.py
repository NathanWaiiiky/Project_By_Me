""" initialisation"""
from Donne_Monde import*
from pygame import mixer
"""initialisation le son pour qu'il n'arache pas les oreilles """
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
"""Music de game over"""
Game_over_sound = pygame.mixer.Sound('Son/Mario_game_over.mp3')
Game_over_sound.set_volume(0.1)
"""fps"""
clock = pygame.time.Clock()
fps = 60

"""nom de la fenêtre"""
pygame.display.set_caption('MarioV2')

"""fenêtre en continue """
encours = True

"""START/EXIT/RESTART"""
start_bouton = Bouton(fen_width // 2 - 350, fen_height // 2, pygame.image.load('Image/Start.png'))
exit_bouton = Bouton(fen_width // 2 + 250, fen_height // 2, pygame.image.load('Image/Exit.png'))

"""Main menu """
Main_menu = True

"""Bg images"""
Bg_img = pygame.image.load('Image/Back_Ground.png')

"""les font"""
font = pygame.font.SysFont('Bauhaus 93', 100)
font_detail = pygame.font.SysFont('Bauhaus 93', 30)

"""couleur blanche"""
white = (255, 255, 255)

""" definir classe joueur"""
player = player(40, 600, World(donne(level_Map)))
"""un seul bowser """
unBowser = 1
"""end defile"""
END_defile= 0

"""jeu"""
while encours == True:
    """fps"""
    clock.tick(fps)
    """back ground fonctionelle  qui avance de 1200 a chaque Level map suplementaire"""
    fen.fill((0, 0, 0))
    fen.blit(Bg_img, (-1200 * player.get_lvl_map(), 0))
    if Main_menu == True:
        pygame.mixer.music.load('Son/Music_Theme_2.mp3')
        pygame.mixer.music.play(-1, 0.0, 5000)
        pygame.mixer.music.set_volume(0.05)
        """Start bouton"""
        if start_bouton.draw():
            Main_menu = False
            """game over"""
            game_over = 0
            """level"""
            player.set_lvl_map(0)
            """Vérification du monde"""
            set_verif(0)
            """temp de depart """
            temp_depart = time.time()
        """Exit Bouton"""
        if exit_bouton.draw():
            encours = False
        """update du player"""
    elif game_over <= 2:
            game_over = player.update(game_over, World(donne(player.get_lvl_map())),Fusee_group, boule_de_feu_bowser_group,Bowser_group)
            """innitialsation du monde"""
            Monde = World(donne(player.get_lvl_map()))
            Monde.draw()
            """lave"""
            Lave_group.draw(fen)
            Lave_group.update()
            """update du Goomba/ draw et du Goomba ecrasée """
            Goomba_group.update(player.getX(),player.getY() + 80,player.get_lvl_map())
            Goomba_group.draw(fen)
            Goomba_ecrasee_group.draw(fen)
            Goomba_ecrasee_group.update()
            """Plante  update / draw"""
            Plante_glace_group.draw(fen)
            Plante_glace_group.update()
            Plante_feux_group.draw(fen)
            Plante_feux_group.update()
            """une plante toute les 10sec"""
            plant_spwan(player.get_lvl_map())
            """boule de feu"""
            Boule_de_feu_group.draw(fen)
            Boule_de_feu_group.update(player.get_lvl_map())
            """boule de glace"""
            Boule_de_glace_group.draw(fen)
            Boule_de_glace_group.update()
            """skip lvl"""
            key = pygame.key.get_pressed()
            if key[pygame.K_p]:
                player.set_lvl_map(6)
                set_verif(6)
            """bowser"""
            if player.get_lvl_map() == 6:
                if unBowser == 1:
                    game_over= 0
                    Bowser_entity = Bowser(840, 380)
                    Bowser_group.add(Bowser_entity)
                    unBowser += 1
                Bowser_group.draw(fen)
                Bowser_group.update()
                """qu'on puisse voir le temp de recharge Fusee / BF et la vie"""
                Affiche('Vie: ' + str(get_Life()), font_detail, white, 860,20)
                Affiche('Recharge de la fusée: ' + truncate(get_tps_Fusee() - time.time(), 1), font_detail,white, 860, 40)
                Affiche('Recharge de la boule de feu: ' + truncate(get_tps_bf() - time.time(), 1), font_detail, white, 860, 60)
            """bowser BF"""
            boule_de_feu_bowser_group.draw(fen)
            boule_de_feu_bowser_group.update()
            """Bowser Fusee"""
            Fusee_group.draw(fen)
            Fusee_group.update()
            """Porte"""
            Porte_group.draw(fen)
            """qu'on puisse voir note vie"""
            Affiche('Vie: '+str(3-game_over), font_detail, white, 20, 20)
            """qu'on puisse voir le temp du pouvoir """
            Affiche('temp du pouvoir restant : ' + truncate(player.get_pouvoir() - time.time(),1),font_detail ,white, 20, 40)
            """temp du parcour"""
            temp_parcours = time.time()-temp_depart
    elif game_over == 100:
        """FIN"""
        END_defile += 1
        Affiche('Pour M.BERNARD', font_detail, white, 550, -200 + END_defile)
        Affiche('BREUGNOT Matéo', font_detail, white, 550, -160 + END_defile)
        Affiche('REVERSAT Antoine', font_detail, white, 550, -120 + END_defile)
        Affiche('MIO Nathan', font_detail, white, 550, -80 + END_defile)
        Affiche('Parcours terminé en : '+str(truncate(temp_parcours, 3)+' Seconde'), font_detail, white, 550, 0 + END_defile)
        Affiche('END', font, white, 550, 80 + END_defile)
    else:
        """music de game_over"""
        Game_over_sound.play()

        """pouvoir reinitialiser"""
        player.set_pouvoir(time.time())
        """retour menu"""
        Main_menu =True
        """reinitialise les goomba"""
        player.set_lvl_map(1)
        Goomba_group.update(player.getX(),player.getY() + 80,player.get_lvl_map())
    """ferme le jeu """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encours = False
    pygame.display.update()
pygame.quit()
