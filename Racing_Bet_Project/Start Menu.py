import pygame as pg
import sys
import os

class Window_Resize:
    def __init__(self, current_size):
        self.w, self.h = current_size

    def Full_Screen(self, screen):
        screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
        self.w, self.h = screen.get_size()
        return screen


    def Window(self, current_size):
        self.w, self.h = current_size
        return pg.display.set_mode((self.w, self.h))
   
class Button():
    def __init__(self, image, pos, text_info, font, base_color, hovering_color) -> None:
        self.image = image
        (self.x_pos, self.y_pos) = pos 
        self.text_info = text_info
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_info, True, self.base_color)

        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def Change_Color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.text = self.font.render(self.text_info, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_info, True, self.base_color)

    def Input_Check(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def Update(self, screen):
        screen.blit(self.text, self.text_rect)
        screen.blit(self.image, self.rect)
    
pg.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
pg.display.set_caption("Funni Game")
size = Window_Resize(screen.get_size())
bg_pos = 0
def Font(size):
    return pg.font.Font(None, size)



def Start_Menu():
    while True:
        mouse_pos = pg.mouse.get_pos()

        Play_Button = Button(pg.image.load("Assets/icon/Obstacles/frame_box.png").convert_alpha(), 
                             (size.w/2, size.h*0.6), "Play", Font(80), "Black", "Blue")
        Options_Button = Button(pg.image.load("Assets/icon/Obstacles/frame_box.png").convert_alpha(), 
                             (size.w/2, size.h*0.75), "Options", Font(80), "Black", "Blue")
        Quit_Button = Button(pg.image.load("Assets/icon/Obstacles/frame_box.png").convert_alpha(), 
                             (size.w/2, size.h*0.9), "Quit", Font(80), "Black", "Blue")
        
        screen.fill('white')
        Title = Font(200).render("Bezt Gem Ever", True, "Gold")
        Title_rect = Title.get_rect(center = (size.w/2, size.h*0.25))
        screen.blit(Title, Title_rect)
        print(Play_Button)


        for button in [Play_Button, Options_Button, Quit_Button]:
            button.Change_Color(mouse_pos)
            button.Update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if Play_Button.Input_Check(mouse_pos):
                    Game(True)
                if Options_Button.Input_Check(mouse_pos):
                    Options()
                if Quit_Button.Input_Check(mouse_pos):
                    pg.quit()
                    sys.exit()

        pg.time.Clock().tick(30)
        pg.display.update()

def Options():
    global screen
    while True:
        screen.fill('Gold')


        Full_Screen = Button(pg.image.load("Assets/icon/Obstacles/frame_box.png").convert_alpha(), 
                             (size.w/2, size.h*0.2), "Full Screen", Font(80), "Black", "Blue")
        HD_Screen = Button(pg.image.load("Assets/icon/Obstacles/frame_box.png").convert_alpha(), 
                             (size.w/2, size.h*0.4), "1280x720", Font(80), "Black", "Blue")
        Small_Screen = Button(pg.image.load("Assets/icon/Obstacles/frame_box.png").convert_alpha(), 
                             (size.w/2, size.h*0.6), "800x600", Font(80), "Black", "Blue")
        Go_Back = Button(pg.image.load("Assets/icon/Obstacles/frame_box.png").convert_alpha(), 
                             (size.w/2, size.h*0.8), "Back", Font(80), "Black", "Blue")

        mouse_pos = pg.mouse.get_pos()
        for button in [Full_Screen, HD_Screen, Small_Screen, Go_Back]:
            button.Change_Color(mouse_pos)
            button.Update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if Full_Screen.Input_Check(mouse_pos):
                    screen = size.Full_Screen(screen)

                if HD_Screen.Input_Check(mouse_pos):
                    screen = size.Window((1280, 720))

                if Small_Screen.Input_Check(mouse_pos):
                    screen = size.Window((800, 600))

                if Go_Back.Input_Check(mouse_pos):
                    Start_Menu()
                    

        pg.display.update()
        pg.time.Clock().tick(30)

def Game(Game_Active):
    global bg_pos

    def Back_Ground_Loop(bg, bg_pos):
        screen.blit(bg, (bg_pos,0))
        screen.blit(bg, (bg_pos + size.w,0))

    while True:
        bg = pg.transform.scale(pg.image.load("Assets/background/sky/sky-1.png").convert(), (size.w,size.h))

        if Game_Active:
            bg_pos -= 4 * size.w/1500

            if bg_pos <= - size.w:
                bg_pos = 0

            Back_Ground_Loop(bg, bg_pos)
            text = Font(120).render("Press ESC to return", True, "Blue")
            text_rect = text.get_rect(center = (size.w/2, size.h /4))
            screen.blit(text, text_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if (event.type == pg.KEYDOWN):
                if (event.key == pg.K_ESCAPE):
                    Start_Menu()

        pg.display.update()
        pg.time.Clock().tick(60)
Start_Menu()
