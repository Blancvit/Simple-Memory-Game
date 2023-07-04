import pygame
import random

Tiles_Color = (140, 120, 81)
Selected_TileColor = (234, 221, 207)
Text_surfaceColor=(0,0,0)
validator=1


class Button:
    def __init__(self, text, x_pos, y_pos, color):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color

    def draw(self):
        font = pygame.font.Font('poppins-semibold.otf', 22)
        button_text = font.render(self.text, True, "black")
        button_rect = pygame.Rect((self.x_pos, self.y_pos), (280, 40))
        pygame.draw.rect(screen, (self.color), button_rect, 0, 3)  # Change button color here
        pygame.draw.rect(screen, (button_Border), button_rect, 2, 3)
        text_rect = button_text.get_rect()
        text_rect.center = button_rect.center
        screen.blit(button_text, text_rect)

    def Get_rect(self):
        button_rect = pygame.Rect((self.x_pos, self.y_pos), (280, 40))
        return button_rect

pygame.init()
screen = pygame.display.set_mode((500, 500))
background = pygame.image.load('Game-BackgroundV1.jpg')
logo=pygame.image.load('logo2-edited.png')
logo_x = (screen.get_width() - 500) // 2
logo_x = (screen.get_width() - 500) // 2
clock = pygame.time.Clock()
running = True
dt = 0

# Button-related code
pygame.display.set_caption('Memory Game')
pygame.display.set_icon(logo)
button_posX = (screen.get_width() - 280) // 2
button_Border = (140, 120, 81)
button_color = (234, 221, 207)
button_hover = (255, 255, 255)

buttons_home = [
    Button('Basic Mode', button_posX, 280, button_color),
    Button('Advanced Mode', button_posX, 330, button_color),
    Button('Instruction', button_posX, 380, button_color),
    Button('Leaderboard', button_posX, 430, button_color),
]
button_rects_home = [button.Get_rect() for button in buttons_home]

# Main game loop
class gameLooper():
    def __init__(self, Game_Start, Game_Mode):
        self.Game_Start=Game_Start
        self.Game_Mode=Game_Mode
Game_Stats=gameLooper(Game_Start=False ,Game_Mode='home')

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(background, (0, 0))
    screen.blit(logo,(logo_x, -125))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if  Game_Stats.Game_Start==False and Game_Stats.Game_Mode=='home':
            for button, button_rect in zip(buttons_home, button_rects_home):
                if button_rect.collidepoint(mouse_pos):
                    button.color = button_hover
                    button.draw()
                    if pygame.mouse.get_pressed()[0] and button.text == button.text:
                        Game_Stats.Game_Start = True
                        Game_Stats.Game_Mode = button.text    
                else:
                    button.color = button_color
                    button.draw()
        elif Game_Stats.Game_Start==True and Game_Stats.Game_Mode=='Basic Mode':
            button_posX = (screen.get_width() - 280) // 2
            class Button2:
                def __init__(self, text, x_pos, y_pos, color):
                    self.text = text
                    self.x_pos = x_pos
                    self.y_pos = y_pos
                    self.color = color

                def draw(self):
                    font = pygame.font.Font('poppins-semibold.otf', 22)
                    button_text = font.render(self.text, True, "black")
                    button_rect = pygame.Rect((self.x_pos, self.y_pos), (280, 40))
                    pygame.draw.rect(screen, (self.color), button_rect, 0, 3)  # Change button color here
                    pygame.draw.rect(screen, (button_Border), button_rect, 2, 3)
                    text_rect = button_text.get_rect()
                    text_rect.center = button_rect.center
                    screen.blit(button_text, text_rect)

                def Get_rect(self):
                    button_rect = pygame.Rect((self.x_pos, self.y_pos), (280, 40))
                    return button_rect
            
            
            class Tile (pygame.sprite.Sprite):
                def __init__(self, width,height,pos_x,pos_y,color,is_correct,is_selected):
                    super().__init__()
                    self.image = pygame.Surface([width, height])
                    self.image.fill(color)
                    self.rect =self.image.get_rect()
                    self.rect.center=[pos_x,pos_y]
                    self.right=False
                    self.is_correct= is_correct
                    self.is_selected=is_selected

            Tile_Group=pygame.sprite.Group()
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
                    New_Tile=Tile(S_width,S_height,T_posx,T_posy,(Tiles_Color),is_correct,is_selected=False)
                    Tile_Group.add(New_Tile)
                    TileColumn+=1
                T_posy+=51
                TileRow+=1

            TileChoice=0
            TileNumber=5
            while TileChoice < TileNumber:
                Selected_Tile = random.choice(Tile_Group.sprites())
                if not Selected_Tile.is_correct:
                    Selected_Tile.is_correct=True
                    Selected_Tile.image.fill(Selected_TileColor)
                    TileChoice+=1

            #timer
            start_time=pygame.time.get_ticks()
            time_limit=5000
            countdown_time = 3000 
            countdown_start = pygame.time.get_ticks()
            points=0
            rightGuess=0
            Level=1
            wrong_clicked=False

            def NextLevel(points, TileNumber):
                global rightGuess
                global time_limit
                global start_time
                start_time = pygame.time.get_ticks()
                rightGuess = 0
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
                global wrong_clicked
                wrong_clicked=False
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

            while running:
                current_time=pygame.time.get_ticks()
                elapsed_time=current_time-start_time
                mouse_pos=pygame.mouse.get_pos()
                buttons = [
                    Button2('Restart', button_posX, 380, button_color),
                    Button2('Home', button_posX, 430, button_color),
                ]
                button_rects = [button.Get_rect() for button in buttons]
                                                                
            
                if elapsed_time <= time_limit:
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                    for sprite in Tile_Group:
                        pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
                        if sprite.is_correct:
                            sprite.image.fill(Selected_TileColor) 
                            pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
                            
                else:
                    for sprite in Tile_Group:
                        if sprite.is_correct and not sprite.is_selected:
                            sprite.image.fill(Tiles_Color)
                            pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                pygame.quit()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos=pygame.mouse.get_pos()
                                for sprite in Tile_Group:
                                    if sprite.rect.collidepoint(mouse_pos) and not sprite.is_selected:
                                        sprite.is_selected=True
                                        if sprite.is_correct:
                                            sprite.image.fill(Selected_TileColor)
                                            pygame.draw.rect(sprite.image, (Tiles_Color), sprite.image.get_rect(), 2)
                                            points+=10
                                            rightGuess+=1
                                            Scoretext = font.render(" Points: "+str(points) , True, (0, 0, 0))
                                            if rightGuess==TileNumber:
                                                if time_limit>1000:
                                                    NextLevel(points,TileNumber)
                                                    time_limit-=1000
                                                    Level+=1
                                                elif time_limit==1000:
                                                    TileNumber+=1
                                                    Level+=1
                                                    NextLevel(points,TileNumber)

                                        elif not sprite.is_correct:
                                            wrong_clicked=True
                                            # Save Highscore
                                            try:
                                                high_score_file = open("high_score.txt", "r")
                                                top_scores = [0, 0, 0, 0, 0, 0]
                                                count = 0
                                                for line in high_score_file:
                                                    line_score = line.rstrip()
                                                    top_scores[count] = int(line_score)
                                                    count += 1
                                                top_scores[5] = points
                                                top_scores.sort(reverse=True)
                                                if top_scores[5]:
                                                    top_scores.pop()
                                                high_score_file.close()
                                                
                                                high_score_file = open("high_score.txt", "w")
                                                for i in range(5):
                                                    stringscore = str(top_scores[i]) + '\n'
                                                    high_score_file.write(stringscore)
                                                high_score_file.close()
                                            except IOError:
                                                print("Unable to save the high score.")
                                            for sprite in Tile_Group:
                                                sprite.is_selected=True    
                if  wrong_clicked:
                    
                        
                    # Show Buttons
                    for button, button_rect in zip(buttons, button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            button.color = button_hover
                            button.draw()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if button.text == 'Restart':
                                    points=0
                                    TileNumber=5
                                    time_limit=5000
                                    Level=1
                                    ResetLevel(points,TileNumber)
                                    wrong_clicked=False    

                                elif button.text=='Home':
                                    Game_Stats.Game_Start=False
                                    Game_Stats.Game_Mode='home'
                                    wrong_clicked=False

                        else:
                            button.color = button_color
                            button.draw()

                if  Game_Stats.Game_Start==False and Game_Stats.Game_Mode=='home':
                    break  

                pygame.display.flip()
                screen.blit(background,(0,0))
                font = pygame.font.Font('poppins-semibold.otf', 22)
                countdown_font = pygame.font.Font('poppins-semibold.otf', 53)
                Scoretext = font.render(" Points: "+str(points) , True, (0, 0, 0))
                LevelText = font.render("Level :"+str(Level), True, (0, 0, 0))
                Timer="%.2f" %((time_limit-elapsed_time)*.001)
                if float(Timer)<=0: 
                    Timer="0"
                Timer_text = font.render("Time: " + str(Timer), True, (0, 0, 0))
                screen.blit(LevelText, (400, 10)) 
                screen.blit(Scoretext, (10, 10)) 
                screen.blit(Timer_text, (120, 76))
                Tile_Group.draw(screen)
                dt = clock.tick(60) / 1000
        #advanced Mode Start        
        elif Game_Stats.Game_Start==True and Game_Stats.Game_Mode=='Advanced Mode':
            button_posX = (screen.get_width() - 280) // 2
            class Button3:
                def __init__(self, text, x_pos, y_pos, color):
                    self.text = text
                    self.x_pos = x_pos
                    self.y_pos = y_pos
                    self.color = color

                def draw(self):
                    font = pygame.font.Font('poppins-semibold.otf', 22)
                    button_text = font.render(self.text, True, "black")
                    button_rect = pygame.Rect((self.x_pos, self.y_pos), (280, 40))
                    pygame.draw.rect(screen, (self.color), button_rect, 0, 3)  # Change button color here
                    pygame.draw.rect(screen, (button_Border), button_rect, 2, 3)
                    text_rect = button_text.get_rect()
                    text_rect.center = button_rect.center
                    screen.blit(button_text, text_rect)

                def Get_rect(self):
                    button_rect = pygame.Rect((self.x_pos, self.y_pos), (280, 40))
                    return button_rect
            
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
                
            #Variables
            start_time=pygame.time.get_ticks()
            time_limit=5000
            countdown_time = 3000 
            countdown_start = pygame.time.get_ticks()
            points=0
            rightGuess=0
            Level=1
            wrong_clicked=False

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
                global wrong_clicked
                wrong_clicked=False
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
                mouse_pos=pygame.mouse.get_pos()
                buttons = [
                    Button3('Restart', button_posX, 380, button_color),
                    Button3('Home', button_posX, 430, button_color),
                ]
                button_rects = [button.Get_rect() for button in buttons]

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
                                            if rightGuess == TileNumber:
                                                if time_limit > 1000:
                                                    NextLevel(points, TileNumber)
                                                    time_limit -= 1000
                                                    Level += 1
                                                elif time_limit == 1000:
                                                    TileNumber += 1
                                                    Level += 1
                                                    NextLevel(points, TileNumber)

                                    elif sprite.is_correct and not validator==sprite.its_number or not sprite.is_correct and not validator==sprite.its_number:
                                        wrong_clicked=True
                                        # Save Highscore
                                        try:
                                            high_score_file = open("high_score.txt", "r")
                                            top_scores = [0, 0, 0, 0, 0, 0]
                                            count = 0
                                            for line in high_score_file:
                                                line_score = line.rstrip()
                                                top_scores[count] = int(line_score)
                                                count += 1
                                            top_scores[5] = points
                                            top_scores.sort(reverse=True)
                                            if top_scores[5]:
                                                top_scores.pop()
                                            high_score_file.close()
                                            
                                            high_score_file = open("high_score.txt", "w")
                                            for i in range(5):
                                                stringscore = str(top_scores[i]) + '\n'
                                                high_score_file.write(stringscore)
                                            high_score_file.close()
                                        except IOError:
                                            print("Unable to save the high score.")
                                        for sprite in Tile_Group:
                                            sprite.is_selected=True

                if  wrong_clicked:
                    # Show Buttons
                        for button, button_rect in zip(buttons, button_rects):
                            if button_rect.collidepoint(mouse_pos):
                                button.color = button_hover
                                button.draw()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if button.text == 'Restart':
                                        points=0
                                        TileNumber=5
                                        time_limit=5000
                                        Level=1
                                        ResetLevel(points,TileNumber)
                                        wrong_clicked=False

                                    elif button.text=='Home':
                                        Game_Stats.Game_Mode='home'
                                        Game_Stats.Game_Start=False
                                        wrong_clicked=False

                            else:
                                button.color = button_color
                                button.draw()            
                if  Game_Stats.Game_Start==False and Game_Stats.Game_Mode=='home':
                    break  
                for sprite in Tile_Group:
                    if sprite.is_correct and sprite.is_selected:
                        if wrong_clicked:
                            Selected_TileFont = pygame.font.Font('poppins-semibold.otf', 0)
                            number_position = sprite.rect.centerx - 6, sprite.rect.centery - 16
                            Text_number = Selected_TileFont.render(str(sprite.its_number), True, (Text_surfaceColor))
                            screen.blit(Text_number, number_position)
                        else:    
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
        elif Game_Stats.Game_Start==True and Game_Stats.Game_Mode=='Instruction':
            Instruction=pygame.image.load('Instruction1.png')
            Close_image=pygame.image.load('CB-1.png')
            Hover_CloseImage=pygame.image.load('CB-2.png')
            Instruction_x = (screen.get_width() - 400) // 2
            button_posX=(screen.get_width() - 40) // 2
            button_Border=(140,120,81)
            button_color=(234,221,207)
            button_hover=(255,255,255)
            Selected_Button=(234,221,207)
            
            class Button:
                def __init__(self, text, x_pos, y_pos, color,enabled):
                    self.text = text
                    self.x_pos = x_pos
                    self.y_pos = y_pos
                    self.color = color
                    self.enabled=enabled
                    

                def draw(self):
                    font = pygame.font.Font('poppins-semibold.otf', 20)
                    button_text = font.render(self.text, True, "black")
                    button_rect = pygame.Rect((self.x_pos, self.y_pos), (30, 30))
                    pygame.draw.rect(screen, (self.color), button_rect, 0, 3)  # Change button color here
                    pygame.draw.rect(screen, (button_Border), button_rect, 2, 3)
                    text_rect = button_text.get_rect()
                    text_rect.center = button_rect.center
                    screen.blit(button_text, text_rect)

                def Get_rect(self):
                    button_rect = pygame.Rect((self.x_pos, self.y_pos), (30, 30))
                    return button_rect
        
            #buttons and other things
            buttons_instructions = [
                            Button('1', 315, 420, button_hover,enabled=False),
                            Button('2',355, 420, button_color,enabled=True),
                            Button('3',395,420,button_color,enabled=True)
                            
                        ]
            button_rects_instructions = [button.Get_rect() for button in buttons_instructions]
            class CloseButton:
                def __init__(self, x ,y ,image):
                    self.image=image
                    self.rect=self.image.get_rect()
                    self.rect.topleft= (x,y)
                    
                def draw(self):
                    screen.blit(self.image,(self.rect.x, self.rect.y))
            Close_button=CloseButton(392,25,Close_image)
            while running:

                mouse_pos=pygame.mouse.get_pos()
                screen.blit(background, (0, 0))
                screen.blit(Instruction,(Instruction_x,10))
                Close_button.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            
                # Button drawing code
                for button, button_rect in zip(buttons_instructions, button_rects_instructions):
                    button.draw()
                    if button.enabled:
                        if button_rect.collidepoint(mouse_pos):
                            button.color=button_hover
                            if pygame.mouse.get_pressed()[0]:  # Check for left mouse button click
                                if button.enabled and button.text=='1':
                                    button.enabled=False
                                    button.color=button_hover
                                    Instruction=pygame.image.load('Instruction1.png')
                                    page2=buttons_instructions[1]
                                    page3=buttons_instructions[2]
                                    if page2.enabled==False or page3.enabled==False:
                                        page2.enabled=True
                                        page3.enabled=True
                                elif button.enabled and button.text=='2':
                                    button.enabled=False
                                    button.color=button_hover
                                    Instruction=pygame.image.load('Instruction2.png')
                                    page1=buttons_instructions[0]
                                    page3=buttons_instructions[2]
                                    if page1.enabled==False or page3.enabled==False:
                                        page1.enabled=True
                                        page3.enabled=True
                                elif button.enabled and button.text=='3':
                                    button.enabled=False
                                    button.color=button_hover
                                    Instruction=pygame.image.load('Instruction3.png')
                                    page1=buttons_instructions[0]
                                    page2=buttons_instructions[1]
                                    if page1.enabled==False or page2.enabled==False:
                                        page1.enabled=True
                                        page2.enabled=True
                        else:
                            button.color = button_color
                            button.draw()
                            
                if Close_button.rect.collidepoint(mouse_pos):
                    Close_button.image=Hover_CloseImage
                    if pygame.mouse.get_pressed()[0]:
                        Game_Stats.Game_Mode='home'
                        Game_Stats.Game_Start=False
                        break
                else:
                    Close_button.image=Close_image

            
            
                dt = clock.tick(60) / 1000
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
        elif Game_Stats.Game_Start==True and Game_Stats.Game_Mode=='Leaderboard':
            Leaderboard_Show=pygame.image.load('leaderboard.png')
            Leaderboard_x = (screen.get_width() - 400) // 2
            Close_image=pygame.image.load('CB-1.png')
            Hover_CloseImage=pygame.image.load('CB-2.png')
            font = pygame.font.Font('poppins-semibold.otf', 32)
            try:
                high_score = [0, 0, 0, 0, 0]
                high_score_file = open("high_score.txt", "r")
                for i in range(5):
                    high_score[i] = int(high_score_file.readline())
                high_score_file.close()
                
            except IOError:
                # Error reading file, no high score
                show_high_score = font.render("There is no highscore yet." , True, (0, 0, 0))
                show_high_scoreRect = show_high_score.get_rect()
                screen.blit(show_high_score, ( 250, 250 ) )
                
                pygame.display.flip()
            except ValueError:
                # There's a file there but we don't understand the number.
                show_high_score = font.render("File is corrupted." , True, (0, 0, 0))
            class CloseButton:
                    def __init__(self, x ,y ,image):
                        self.image=image
                        self.rect=self.image.get_rect()
                        self.rect.topleft= (x,y)
                        
                    def draw(self):
                        screen.blit(self.image,(self.rect.x, self.rect.y))
            Close_button=CloseButton(392,25,Close_image)
            while running:
                mouse_pos=pygame.mouse.get_pos()
                screen.blit(background, (0, 0))
                screen.blit(Leaderboard_Show,(Leaderboard_x,10))
                Close_button.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                show_high_score1 = font.render("1.  "+str(high_score[0]), True, (255, 255, 255))
                show_high_score2 = font.render("2.  "+str(high_score[1]), True, (255, 255, 255))
                show_high_score3 = font.render("3.  "+str(high_score[2]), True, (255, 255, 255))
                show_high_score4 = font.render("4.  "+str(high_score[3]), True, (255, 255, 255))
                show_high_score5 = font.render("5.  "+str(high_score[4]), True, (255, 255, 255))
                
                if high_score[0] != 0:
                    screen.blit(show_high_score1, (140, 130))
                if high_score[1] != 0:
                    screen.blit(show_high_score2, (140, 170))
                if high_score[2] != 0:
                    screen.blit(show_high_score3, (140, 210))
                if high_score[3] != 0:
                    screen.blit(show_high_score4, (140, 250))
                if high_score[4] != 0:
                    screen.blit(show_high_score5, (140, 290))
                    
                if Close_button.rect.collidepoint(mouse_pos):
                    Close_button.image=Hover_CloseImage
                    if pygame.mouse.get_pressed()[0]:
                        Game_Stats.Game_Mode='home'
                        Game_Stats.Game_Start=False
                        break
                else:
                    Close_button.image=Close_image

                pygame.display.flip()       
                dt = clock.tick(60) / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

        pygame.display.flip()       
        dt = clock.tick(60) / 1000

pygame.quit()
