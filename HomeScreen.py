import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
background = pygame.image.load('Game-BackgroundV1.jpg')
Instruction=pygame.image.load('Instruction1.png')
Instruction_x = (screen.get_width() - 400) // 2
button_posX=(screen.get_width() - 40) // 2
button_Border=(140,120,81)
button_color=(234,221,207)
button_hover=(255,255,255)
Selected_Button=(234,221,207)
clock = pygame.time.Clock()
running = True
dt = 0

pygame.display.set_caption('Memory Game')

class Button:
    def __init__(self, text, x_pos, y_pos, color,enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.enabled=enabled
        

    def draw(self):
        font = pygame.font.Font("poppins-semibold.otf", 20)
        button_text = font.render(self.text, True, "black")
        button_rect = pygame.Rect((self.x_pos, self.y_pos), (30, 30))
        pygame.draw.rect(screen, (self.color), button_rect, 0, 3)  # Change button color here
        pygame.draw.rect(screen, (button_Border), button_rect, 2, 3)
        text_rect = button_text.get_rect()
        text_rect.center = button_rect.center
        screen.blit(button_text, text_rect)

    def Get_rect(self):
        button_rect = pygame.Rect((self.x_pos, self.y_pos), (40, 40))
        return button_rect
 #buttons and other things
buttons = [
                Button('1', 315, 420, button_hover,enabled=False),
                Button('2',355, 420, button_color,enabled=True),
                Button("3",395,420,button_color,enabled=True)
            ]
button_rects = [button.Get_rect() for button in buttons]

while running:

    mouse_pos=pygame.mouse.get_pos()
    screen.blit(background, (0, 0))
    screen.blit(Instruction,(Instruction_x,10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Button drawing code
    for button, button_rect in zip(buttons, button_rects):
        button.draw()
        if button.enabled:
            if button_rect.collidepoint(mouse_pos):
                button.color=button_hover
                if pygame.mouse.get_pressed()[0]:  # Check for left mouse button click
                    if button.enabled and button.text=='1':
                        button.enabled=False
                        button.color=button_hover
                        Instruction=pygame.image.load('Instruction1.png')
                        page2=buttons[1]
                        page3=buttons[2]
                        if page2.enabled==False or page3.enabled==False:
                            page2.enabled=True
                            page3.enabled=True
                    elif button.enabled and button.text=='2':
                        button.enabled=False
                        button.color=button_hover
                        Instruction=pygame.image.load('Instruction2.png')
                        page1=buttons[0]
                        page3=buttons[2]
                        if page1.enabled==False or page3.enabled==False:
                            page1.enabled=True
                            page3.enabled=True
                    elif button.enabled and button.text=='3':
                        button.enabled=False
                        button.color=button_hover
                        Instruction=pygame.image.load('Instruction3.png')
                        page1=buttons[0]
                        page2=buttons[1]
                        if page1.enabled==False or page2.enabled==False:
                            page1.enabled=True
                            page2.enabled=True
            else:
                button.color = button_color
                button.draw()
                
    dt = clock.tick(60) / 1000
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()