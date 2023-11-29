import pygame as pg
import sys
import os
from math import sin, radians as rad

#class to get current screen info and resize the windows base on the options
class Screen_Info:
    def __init__(self, current_size):
        self.w, self.h = current_size

    def Full_Screen(self):
        pg.display.set_mode((0,0), pg.SRCALPHA|pg.FULLSCREEN)
        self.w, self.h = screen.get_size()

    def Window(self, current_size):
        self.w, self.h = current_size
        pg.display.set_mode((self.w, self.h))

#class to create little circles for mouse click
class Mouse_Animation(pg.sprite.Sprite):
    def __init__(self, instant_mouse_pos, r, size) -> None:
        super().__init__()
        self.r = r
        self.size = size
        self.transparency = 255
        self.pos = instant_mouse_pos
        self.image = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/Circle.png').convert_alpha(), 0, 0.005 * self.r)
        self.rect = self.image.get_rect(center = (self.pos))
    
    def Kill(self):
        if self.r >= 75 * self.size/1280:
            self.kill()
        
    def update(self):
        self.r += 3.5 * self.size/1280
        self.transparency -= 255 * (3.5 / 70)
        self.image = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/Circle.png').convert_alpha(), 0, 0.005 * self.r)
        self.image.set_alpha(self.transparency)
        self.rect = self.image.get_rect(center = (self.pos))
        self.Kill()

class Dynamic_Background():
    def __init__(self, bg, size, mouse_pos):
        self.image = bg
        self.x, self.y = size
        self.mouse_x, self.mouse_y = mouse_pos
        self.rect = self.image.get_rect(center = (self.x,  self.y))

    def Draw(self):
        self.rect = self.image.get_rect(center = (self.x + 0.075 * self.mouse_x, self.y + 0.075 * self.mouse_y))
        screen.blit(self.image, self.rect)

#class that control all of the interactive buttons
class Button():
    def __init__(self, pos, image, hovering_image = None, text_info = None, 
                 font = None, base_color = None, hovering_color =  None):
        self.image = image
        (self.x_pos, self.y_pos) = pos 

        if text_info == None:
            self.hovering_image = hovering_image

            self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
            self.rect02 = self.hovering_image.get_rect(center = (self.x_pos, self.y_pos))

        else:
            self.text_info = text_info
            self.font = font
            self.base_color = base_color
            self.hovering_color = hovering_color
            self.text = self.font.render(self.text_info, True, self.base_color)

            self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
    
    def Change_Image(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hovering_image, self.rect02)
        else:
            screen.blit(self.image, self.rect)

    def Change_Text_Color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.text = self.font.render(self.text_info, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_info, True, self.base_color)

    def Input_Check(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def Update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pg.display.set_mode((1280,720), pg.SRCALPHA)
pg.display.set_caption("Racing Bet")

size = Screen_Info(screen.get_size()) #get initial screen size
mouse_animation = pg.sprite.Group() #group for mouse animation

timer = pg.USEREVENT + 1
pg.time.set_timer(timer, 1000)
#func for fonts
def Font(size):
    return pg.font.Font(None, size)

def Start_Animation():
    transparency = -100
    counter = 0
    while True:
        counter += 1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
            
        
        logo = pg.transform.scale(pg.image.load('Assets/icon/Settings/Logo HCMUS.png'), (size.w / 3, size.w / 3))
        logo_rect = logo.get_rect(center = (size.w/2, size.h/2))
        screen.fill(0)

        transparency += 4
        if transparency < 180 and transparency > 0:
            logo.set_alpha(int(255 * sin(rad(transparency))))
            screen.blit(logo, logo_rect)
        elif transparency > 250:
            mouse_animation.empty()
            Login_Page()

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(120)
        pg.display.update()

#Login_Page
def Login_Page():
    counter = 0
    while True:
        counter += 1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                Start_Menu()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))

        bg = pg.transform.scale(pg.image.load('Assets/background/Street/citystreet.png'), (size.w*1.15, size.h*1.15))
        bg = pg.transform.smoothscale(bg, (128, 72))
        bg = pg.transform.smoothscale(bg, (size.w * 1.15, size.h * 1.15))
        background = Dynamic_Background(bg, (size.w/2, size.h/2), mouse_pos)
        background.Draw()

        pg.draw.rect(screen, "lightblue", (size.w*0.125, size.h*0.125, size.w * 0.75, size.h * 0.75))

        Login = pg.transform.scale(pg.image.load('Assets/icon/Settings/user_icon01.png').convert_alpha(), 
                                (size.w*0.375 / 2, size.h*0.1))
        Login_hover = pg.transform.scale(pg.image.load('Assets/icon/Settings/user_icon02.png').convert_alpha(), 
                                        (size.w*0.375 / 2, size.h*0.1)) 
        Login_tab = Button((size.w * 0.3, size.h * 0.175), Login, Login_hover)

        Login_tab.Change_Image(mouse_pos)
            
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(120)
        pg.display.update()
        
def Start_Menu():
    temp = 0
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Quit.Input_Check(mouse_pos):
                    pg.quit()
                    sys.exit()
                if User.Input_Check(mouse_pos):
                    pass
                if Setting.Input_Check(mouse_pos):
                    mouse_animation.empty()
                    Options()
        #Get the assets to draw on the screen
        bg = pg.transform.scale(pg.image.load('Assets/background/Street/citystreet.png'), (size.w*1.15, size.h*1.15))
        background = Dynamic_Background(bg, (size.w/2, size.h/2), mouse_pos)
        background.Draw()

        temp += 0.1
        Title = Font(int(150 * size.w / 1280)).render("Racing Bet", True, "Black")
        Title_box = Title.get_rect(center = (size.w * 0.5,size.h *(0.25 + 0.04 * sin(temp))))

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
        screen.blit(Title, Title_box)
        screen.blit(Prompt, Prompt_box)
        Quit.Change_Image(mouse_pos)
        User.Change_Image(mouse_pos)
        Setting.Change_Image(mouse_pos)

        mouse_animation.update()
        mouse_animation.draw(screen)
        
        pg.time.Clock().tick(120)
        pg.display.update()

def Options():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Full_Screen.Input_Check(mouse_pos):
                    size.Full_Screen()

                if HD_Screen.Input_Check(mouse_pos):
                    size.Window((1280, 720))

                if Small_Screen.Input_Check(mouse_pos):
                    size.Window((800, 600))

                if Go_Back.Input_Check(mouse_pos):
                    Start_Menu()
        Bg = pg.transform.scale(pg.image.load("Assets/background/sky/sky-3.png"), (size.w, size.h))
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


        pg.display.update()
        pg.time.Clock().tick(120)
Start_Animation()