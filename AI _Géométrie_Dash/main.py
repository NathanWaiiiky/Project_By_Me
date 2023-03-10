from The_game import*
# fps
clock = pygame.time.Clock()
fps = 60

# window
pygame.display.set_caption('Geometrie_Dash')

# BackGround
Bg_img = pygame.image.load('image/Bg.png' )
i = 0

# continously window
encours = True

# Start
Start = False

# Menu
start_button = Bouton(fen_width // 2 - 60, fen_height // 2, pygame.image.load('Image/Start.png'))
# Font

font = pygame.font.SysFont('Bauhaus 93', 100)
font_detail = pygame.font.SysFont('Bauhaus 93', 30)

# Generation
Generation = 0
# AI

AI = [['B', 681, 571], ['P', 624, 535], ['PR', 699, 498]]
BestAI=[]
BestTimer=0
Newx=0
Newy=0
NewAI=[]
# The Game

while encours:
    clock.tick(fps)
    fen.fill((0, 0, 0))
    fen.blit(Bg_img, (i, 0))
    fen.blit(Bg_img, (fen_width + i, 0))
    i -= 8
    if i == -fen_width:
        fen.blit(Bg_img, (fen_width+i, 0))
        i = 0

    if Main_menu:
        # Start button
        if start_button.draw() or play:
            Main_menu = False
            play = False
        Start = False
    else:
        if not Start:
            Attempt,Pike_group,Brick_group = start(Attempt)
        else:
            # Monde
            Monde = World(grille_jeu(jeu_Pike(),jeu_Brick()))
            Monde.draw()
            # Player Sprite
            Main_menu, Endtime = Player.update(Main_menu, Monde.get_list(), Start)
            # Brick
            Brick_group.draw(fen)
            Brick_group.update()
            # Pike
            Pike_group.draw(fen)
            Pike_group.update()
            # Score and Generation
            Score('Generation : ' + str(Generation), font_detail, (255, 255, 255), 20, 20)
            Score('Score : ' + (Endtime),font_detail , (255, 255, 255),20, 40)
            #Neurons
            Brick_Neurons_group.draw(fen)
            Brick_Neurons_group.update()
            Pike_Neurons_group.draw(fen)
            Pike_Neurons_group.update()
            # neurons Red
            Brick_Neurons_group_R.draw(fen)
            Brick_Neurons_group_R.update()
            Pike_Neurons_group_R.draw(fen)
            Pike_Neurons_group_R.update()
            # ______________________AI_________________________
            T=Get_Time(Main_menu, Endtime)
            if Main_menu:
                if float(T) >float(BestTimer):
                    BestTimer = T
                    BestAI = AI
                    print(BestAI)
                for I in range(len(AI)):
                    PartAI=[]
                    for J in range(len(AI[I])):
                        if J>0:
                            PartAI.append(AI[I][J]+random.randint(-10,10))
                        else:
                            PartAI.append(AI[I][J])
                    NewAI.append(PartAI)
                #add a new neurons
                AI = NewAI
                NewAI = []
                play = True
                Pike_Neurons_group = pygame.sprite.Group()
                Brick_Neurons_group = pygame.sprite.Group()
                Pike_Neurons_group_R = pygame.sprite.Group()
                Brick_Neurons_group_R = pygame.sprite.Group()
                if Attempt >=100:
                    Generation+=1
                    Attempt=0
                    AI = BestAI.copy()
                    AI.append(Random_one_Neurons())
                Create_Ai(AI, Pike_Neurons_group, Brick_Neurons_group,Pike_Neurons_group_R, Brick_Neurons_group_R)

        Start = True
        # end the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encours = False
    pygame.display.update()
pygame.quit()
