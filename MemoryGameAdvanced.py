import pygame
import random
Text_surfaceColor=(0,0,0)
validator=1
Tiles_Color= (140,120,81)
Selected_TileColor=(234,221,207)

class Tile (pygame.sprite.Sprite):
    def __init__(self, width,height,pos_x,pos_y,color,is_correct,is_selected,its_number):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect =self.image.get_rect()
        self.rect.center=[pos_x,pos_y]
        self.right=False
        self.is_correct= is_correct
        self.is_selected=is_selected
        self.font= pygame.font.Font('poppins-semibold.otf', 22)
        self.its_number=its_number
       
#pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
background=pygame.image.load('Game-BackgroundV1.jpg')
clock = pygame.time.Clock()
running = True
dt = 0

#tile_group
Tile_Group=pygame.sprite.Group()
Tile_Group
S_height=50
S_width=50
T_posy=130
TileRow=1

while TileRow<=5:
    TileColumn=1
    T_posx=95
    while TileColumn<=5:
        T_posx+=51
        is_correct=False#Set to true if in randomizer
        New_Tile=Tile(S_width,S_height,T_posx,T_posy,(Tiles_Color),is_correct,is_selected=False,its_number=0)
        Tile_Group.add(New_Tile)
        TileColumn+=1
    T_posy+=51
    TileRow+=1

#TileRandomizer
TileChoice=0
TileNumber=5
while TileChoice < TileNumber:
    Selected_Tile = random.choice(Tile_Group.sprites())
    if not Selected_Tile.is_correct:
        Selected_Tile.is_correct=True
        Selected_Tile.image.fill(Selected_TileColor)
        TileChoice+=1
        Selected_Tile.its_number=TileChoice
        Selected_Tile.its_numberVerifier=False
    
#timer
start_time=pygame.time.get_ticks()
time_limit=5000
countdown_time = 3000 
countdown_start = pygame.time.get_ticks()
points=0
rightGuess=0
Level=1

def NextLevel(points, TileNumber):
    global rightGuess
    global time_limit
    global start_time
    global validator
    start_time = pygame.time.get_ticks()
    rightGuess = 0
    validator = 1
    points = points
    TileNumber = TileNumber

    for tile in Tile_Group:
        tile.is_selected = False
        tile.is_correct = False
        tile.image.fill(Tiles_Color)

    # Generate new random tiles for the next level
    TileChoice = 0
    while TileChoice < TileNumber:
        Selected_Tile = random.choice(Tile_Group.sprites())
        if not Selected_Tile.is_correct:
            Selected_Tile.is_correct = True
            Selected_Tile.image.fill(Selected_TileColor)
            TileChoice += 1
            Selected_Tile.its_number=TileChoice

    # Hide the tiles during the countdown
    for sprite in Tile_Group:
        sprite.image.fill(Tiles_Color)
        pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)

    # Display countdown before proceeding to the next level
    countdown_time = 3000  # 3 seconds in milliseconds
    countdown_start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - countdown_start < countdown_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.blit(background, (0, 0))
        screen.blit(LevelText, (400, 10)) 
        screen.blit(Scoretext, (10, 10)) 
        Tile_Group.draw(screen)
        countdown_remaining = (countdown_time - (pygame.time.get_ticks() - countdown_start)) // 1000 + 1
        countdown_text = countdown_font.render(str(countdown_remaining), True, (255, 0, 0))
        screen.blit(countdown_text, (233, 350))
        pygame.display.flip()
        clock.tick(60)

    # Reveal the tiles after the countdown
    for sprite in Tile_Group:
        if sprite.is_correct:
            sprite.image.fill(Selected_TileColor)

    start_time = pygame.time.get_ticks()
   
def ResetLevel(points, TileNumber):
    global time_limit
    global start_time
    global rightGuess
    global validator
    validator=1
    start_time=pygame.time.get_ticks()
    rightGuess=0
    points = points
    TileNumber=TileNumber
    for tile in Tile_Group:
        tile.is_selected = False
        tile.is_correct = False
        tile.image.fill(Tiles_Color)
        pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
    # Generate new random tiles for the next level
    TileChoice = 0
    while TileChoice < TileNumber:
        Selected_Tile = random.choice(Tile_Group.sprites())
        if not Selected_Tile.is_correct:
            Selected_Tile.is_correct = True
            Selected_Tile.image.fill(Selected_TileColor)
            TileChoice += 1
            Selected_Tile.its_number=TileChoice


while running:
    current_time=pygame.time.get_ticks()
    elapsed_time=current_time-start_time
   
    if elapsed_time <= time_limit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for sprite in Tile_Group:
            pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
            if sprite.is_correct:
                Selected_TileFont= pygame.font.Font('poppins-semibold.otf', 22)
                number_position=sprite.rect.centerx-6, sprite.rect.centery-16
                sprite.image.fill(Selected_TileColor)
                Text_number = Selected_TileFont.render(str(sprite.its_number), True,  (0,0,0))
                pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
                screen.blit(Text_number,number_position)
           
    else:
        for sprite in Tile_Group:
            if sprite.is_correct and not sprite.is_selected:
                sprite.image.fill(Tiles_Color)
                pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                for sprite in Tile_Group:
                    if sprite.rect.collidepoint(mouse_pos) and not sprite.is_selected:
                        sprite.is_selected=True
                        if sprite.is_correct and validator==sprite.its_number:
                                validator+=1
                                rightGuess+=1
                                sprite.image.fill(Selected_TileColor)
                                pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
                                points += 10
                                Scoretext = font.render(" Points: "+str(points) , True, ("black"))
                                print(points)
                                print(sprite.its_number)
                                if rightGuess == TileNumber:
                                    if time_limit > 1000:
                                        print("Next Level, Reduce Time!")
                                        NextLevel(points, TileNumber)
                                        time_limit -= 1000
                                        Level += 1
                                    elif time_limit == 1000:
                                        TileNumber += 1
                                        Level += 1
                                        print("Next Level, Add Tiles!")
                                        NextLevel(points, TileNumber)

                        elif sprite.is_correct and not validator==sprite.its_number or not sprite.is_correct and not validator==sprite.its_number:
                            sprite.image.fill("orange")
                            points=0
                            Level=1
                            print("Wrong Tiles!")
                            time_limit=5000
                            TileNumber=5
                            ResetLevel(points,TileNumber)

    
    
   
    for sprite in Tile_Group:
        if sprite.is_correct and sprite.is_selected:
            Selected_TileFont = pygame.font.Font('poppins-semibold.otf', 22)
            number_position = sprite.rect.centerx - 6, sprite.rect.centery - 16
            Text_number = Selected_TileFont.render(str(sprite.its_number), True, (Text_surfaceColor))
            screen.blit(Text_number, number_position)

    pygame.display.flip()
    screen.blit(background,(0,0))
    font = pygame.font.Font('poppins-semibold.otf', 22)
    countdown_font = pygame.font.Font('poppins-semibold.otf', 53)
    Scoretext = font.render(" Points: "+str(points) , True, ("black"))
    LevelText = font.render("Level :"+str(Level), True, ("black"))
    Timer="%.2f" %((time_limit-elapsed_time)*.001)
    if float(Timer)<=0: 
        Timer="0"
    Timer_text = font.render("Time: " + str(Timer), True, ("black"))
    screen.blit(LevelText, (400, 10)) 
    screen.blit(Scoretext, (10, 10)) 
    screen.blit(Timer_text, (120, 76)) 
    
    Tile_Group.draw(screen)
    
    dt = clock.tick(60) / 1000 
pygame.quit() #check