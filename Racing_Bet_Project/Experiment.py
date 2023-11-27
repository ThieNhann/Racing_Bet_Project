import pygame as pg
import sys
import os
import math

class Window_Resize:
    def __init__(self, current_size):
        self.w, self.h = current_size

    def Full_Screen(self):
        pg.display.set_mode((0,0), pg.SRCALPHA|pg.FULLSCREEN)
        self.w, self.h = screen.get_size()

    def Window(self, current_size):
        self.w, self.h = current_size
        pg.display.set_mode((self.w, self.h))

   
class Button():
    def __init__(self, pos, image, hovering_image = None, text_info = None, 
                 font = None, base_color = None, hovering_color =  None):
        if text_info == None:
            self.image = image
            self.hovering_image = hovering_image
            (self.x_pos, self.y_pos) = pos

            self.rect01 = self.image.get_rect(center = (self.x_pos, self.y_pos))
            self.rect02 = self.hovering_image.get_rect(center = (self.x_pos, self.y_pos))
        else:
            self.image = image
            (self.x_pos, self.y_pos) = pos 
            self.text_info = text_info
            self.font = font
            self.base_color = base_color
            self.hovering_color = hovering_color
            self.text = self.font.render(self.text_info, True, self.base_color)

            self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
    
    def Change_Image(self, mouse_pos):
        if self.rect01.collidepoint(mouse_pos):
            screen.blit(self.hovering_image, self.rect02)
        else:
            screen.blit(self.image, self.rect01)

    def Icon_Input_Check(self, mouse_pos):
        if self.rect02.collidepoint(mouse_pos):
            return True
        return False

    def Change_Text_Color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.text = self.font.render(self.text_info, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_info, True, self.base_color)

    def Word_Input_Check(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def Update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pg.display.set_mode((1280, 720), pg.SRCALPHA)
pg.display.set_caption("Funni Game")

size = Window_Resize(screen.get_size())

bg_pos = 0

def Font(size):
    return pg.font.Font(None, size)


def Start_Menu():
    temp = 0
    animation_timer = 0
    instant_mouse_pos = (0,0)

    def Mouse_Animation(r, instant_mouse_pos):
        Circle = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/Circle.png').convert_alpha(), 0, 0.005*r)
        Circle_box = Circle.get_rect(center = (instant_mouse_pos))
        screen.blit(Circle, Circle_box)

    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                animation_timer = 40
                instant_mouse_pos = mouse_pos
                if Quit.Icon_Input_Check(mouse_pos):
                    pg.quit()
                    sys.exit()
                if User.Icon_Input_Check(mouse_pos):
                    pass
                if Setting.Icon_Input_Check(mouse_pos):
                    Options()   
        #Get the assets to draw on the screen
        Bg = pg.transform.scale(pg.image.load("Assets/background/ocean/ocean.png"), (size.w, size.h))

        temp += 0.1
        Title = Font(int(150 * size.w / 1280)).render("Get Broke Simulator", True, "Black")
        Title_box = Title.get_rect(center = (size.w * 0.5, size.h *(0.25 + 0.04 * math.sin(temp))))

        Prompt = Font(int(40 * size.w / 1280)).render("- Click anywhere to enter -", True, "Black")
        Prompt_box = Prompt.get_rect(center = (size.w * 0.5, size.h * 0.75))

        Quit_icon = pg.transform.scale(pg.image.load('Assets/icon/Settings/shut_down01.png').convert_alpha(), 
                                       (60*size.w/1280, 60* size.w/1280))
        Quit_icon_hover = pg.transform.scale(pg.image.load('Assets/icon/Settings/shut_down02.png').convert_alpha(), 
                                             (60*size.w/1280, 60* size.w/1280))
        Quit = Button((size.w * 0.03, size.h * 0.95), Quit_icon, Quit_icon_hover)

        User_icon = pg.transform.scale(pg.image.load('Assets/icon/Settings/user_icon01.png').convert_alpha(), 
                                       (60*size.w/1280, 60* size.w/1280))
        User_icon_hover = pg.transform.scale(pg.image.load('Assets/icon/Settings/user_icon02.png').convert_alpha(), 
                                             (60*size.w/1280, 60* size.w/1280))
        User = Button((size.w * 0.97, size.h * 0.05), User_icon, User_icon_hover)

        Setting_icon = pg.transform.scale(pg.image.load('Assets/icon/Settings/setting01.png').convert_alpha(), 
                                       (60*size.w/1280, 60* size.w/1280))
        Setting_icon_hover = pg.transform.scale(pg.image.load('Assets/icon/Settings/setting02.png').convert_alpha(), 
                                             (60*size.w/1280, 60* size.w/1280))
        Setting = Button((size.w * 0.97, size.h * 0.15), Setting_icon, Setting_icon_hover)

        #draw on the screen
        screen.blit(Bg, (0,0))
        screen.blit(Title, Title_box)
        screen.blit(Prompt, Prompt_box)
        Quit.Change_Image(mouse_pos)
        User.Change_Image(mouse_pos)
        Setting.Change_Image(mouse_pos)

        if animation_timer >= 1:
            animation_timer -= 5
            Mouse_Animation(40 - animation_timer, instant_mouse_pos)
        
        pg.time.Clock().tick(30)
        pg.display.update()


def Options():
    global screen
    animation_timer = 0
    instant_mouse_pos = (0,0)
    def Mouse_Animation(r, instant_mouse_pos):
        Circle = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/Circle.png').convert_alpha(), 0, 0.005*r)
        Circle_box = Circle.get_rect(center = (instant_mouse_pos))
        screen.blit(Circle, Circle_box)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                animation_timer = 40
                instant_mouse_pos = mouse_pos
                if Full_Screen.Word_Input_Check(mouse_pos):
                    size.Full_Screen()

                if HD_Screen.Word_Input_Check(mouse_pos):
                    size.Window((1280, 720))

                if Small_Screen.Word_Input_Check(mouse_pos):
                    size.Window((800, 600))

                if Go_Back.Word_Input_Check(mouse_pos):
                    Start_Menu()

        Bg = pg.transform.scale(pg.image.load("Assets/background/ocean/ocean.png"), (size.w, size.h))
        screen.blit(Bg, (0,0))

        Button_box = pg.transform.scale(pg.image.load('Assets/icon/Settings/Button Box.png').convert_alpha(), 
                                       (450*size.w/1280, 75* size.w/1280))

        Full_Screen = Button((size.w * 0.5, size.h*0.2), Button_box, 
                             None, "Full Screen", Font(int(100 * size.w / 1280)), "Black", "Blue")
        HD_Screen = Button((size.w * 0.5, size.h*0.4), Button_box, 
                             None, "1280x720", Font(int(100 * size.w / 1280)), "Black", "Blue")
        Small_Screen = Button((size.w * 0.5, size.h*0.6), Button_box, 
                              None, "800x600", Font(int(100 * size.w / 1280)), "Black", "Blue")
        Go_Back = Button((size.w * 0.5, size.h*0.8), Button_box, 
                             None, "Back", Font(int(100 * size.w / 1280)), "Black", "Blue")

        mouse_pos = pg.mouse.get_pos()
        for button in [Full_Screen, HD_Screen, Small_Screen, Go_Back]:
            button.Change_Text_Color(mouse_pos)
            button.Update()

        if animation_timer >= 1:
            animation_timer -= 5
            Mouse_Animation(40 - animation_timer, instant_mouse_pos)

        
                    

        pg.display.update()
        pg.time.Clock().tick(30)
Start_Menu()