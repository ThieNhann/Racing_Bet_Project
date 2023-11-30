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


class Draw_Screen():
    def __init__(self, type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, pos):
        self.type = type

        if self.type == 'image':
            self.x, self.y = pos
            self.image_file = image_file
            self.image_scale = image_scaling
            self.image = pg.transform.scale(pg.image.load(self.image_file).convert(), (self.image_scale))
            self.rect = self.image.get_rect(center = (self.x, self.y))

        elif self.type == 'text':
            self.x, self.y = pos
            self.image = False
            self.rect_size = False
            self.font = font
            self.text_content = text_content
            self.color = color
            self.text = self.font.render(self.text_content, True, self.color)
            self.rect = self.text.get_rect(center = (self.x, self.y))

        elif self.type == 'rect':
            self.image = False
            self.text_content = False
            self.color = color
            self.rect_pos = rect_pos
            self.rect_size = rect_size
            self.rect = pg.Rect((self.rect_pos, self.rect_size))
    
    def Blit(self):
        if self.type == 'image':
            screen.blit(self.image, self.rect)

        if self.type == 'text':
            screen.blit(self.text, self.rect)
        
        if self.type == 'rect':
            pg.draw.rect(screen, self.color, self.rect)
        
#class that control all of the interactive buttons
class Button(Draw_Screen):
    def __init__(self, type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, alter_color, pos):
        super().__init__(type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, pos)
        self.alter_color = alter_color

    def Change_Color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.type == 'rect':
                pg.draw.rect(screen, self.alter_color, self.rect)
            elif self.type != 'text' and self.type != 'image':
                pg.draw.rect(screen, self.color, self.rect)

            if self.type == 'text':
                self.text = self.font.render(self.text_content, True, self.alter_color)
                screen.blit(self.text, self.rect)
            elif self.type != 'rect' and self.type != 'image':
                self.text = self.font.render(self.text_content, True, self.color)
                screen.blit(self.text, self.rect)
    
    def Mouse_Hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):  
            return True
        return False

    '''def Input_Check(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False'''
    
    '''def Update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.rect)'''
    
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
    transparency = 180
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

        transparency += 2.5
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
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                #Start_Menu()
                pass
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if (Login_Button.Mouse_Hover(mouse_pos)):
                    print("Sleep time")
                if (signup_select.Mouse_Hover(mouse_pos)):
                    Signup_Page()


        bg = Draw_Screen('image', None, None, 'Assets/background/village/village.png', (size.w*0.75, size.h*0.75), None, None, None, (size.w*0.5, size.h*0.5))
        menu = Draw_Screen('rect', bg.rect.topleft, (size.w*0.375, size.h * 0.75), None, None, None, None, '#424769', None)

        welcome_text = Draw_Screen('text', None, None, None, None, 'Welcome', Font(80), '#ffffff', (size.w * 0.3125, size.h * 0.3))

        login_select = Draw_Screen('text', None, None, None, None, 'Login', Font(30), '#f9b17a', (size.w * 0.265, size.h * 0.178))
        signup_select = Button('text', None, None, None, None, 'Sign up', Font(30), '#676f9d', '#5d648c', (size.w * 0.35, size.h * 0.178))

        username_form = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None)
        password_form = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None)

        username_form_text = Draw_Screen('text', None, None, None, None, 'username', Font(20), '#424769', (size.w * 0.22, size.h * 0.41))
        password_form_text = Draw_Screen('text', None, None, None, None, 'password', Font(20), '#424769', (size.w * 0.22, size.h * 0.54))

        forgot_password = Button('text', None, None, None, None, 'Forgor password?', Font(20), '#676f9d', '#d69869', (size.w * 0.405, size.h * 0.64))

        Login_Button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None)
        FaceID_Button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None)

        Login_Button_text = Draw_Screen('text', None, None, None, None, 'Login', Font(30), '#424769', (size.w * 0.225, size.h * 0.73))
        FaceID_Button_text = Draw_Screen('text', None, None, None, None, 'Face ID', Font(30), '#424769', (size.w * 0.395, size.h * 0.73))

        screen.fill('#2d3250')
        bg.Blit()
        menu.Blit()

        login_select.Blit()
        signup_select.Blit()
        welcome_text.Blit()

        username_form.Blit()
        password_form.Blit()
        forgot_password.Blit()
        Login_Button.Blit()
        FaceID_Button.Blit()

        for button in [signup_select, username_form, password_form, Login_Button, FaceID_Button]:
            button.Change_Color(mouse_pos)
        
        username_form_text.Blit()
        password_form_text.Blit()
        Login_Button_text.Blit()
        FaceID_Button_text.Blit()

        
        #pg.draw.line(screen, "White", (0, size.h/2), (size.w, size.h/2))
        #pg.draw.line(screen, "White", (size.w * 0.3125, 0), (size.w * 0.312, size.h))
        
        pg.time.Clock().tick(120)
        pg.display.update()

def Signup_Page():
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                #Start_Menu()
                pass
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if (Login_Button.Mouse_Hover(mouse_pos)):
                    print("Spooky")
                if(login_select.Mouse_Hover(mouse_pos)):
                    Login_Page()


        bg = Draw_Screen('image', None, None, 'Assets/background/village/village.png', (size.w*0.75, size.h*0.75), None, None, None, (size.w*0.5, size.h*0.5))
        menu = Draw_Screen('rect', bg.rect.topleft, (size.w*0.375, size.h * 0.75), None, None, None, None, '#424769', None)

        welcome_text = Draw_Screen('text', None, None, None, None, 'Welcome', Font(80), '#ffffff', (size.w * 0.3125, size.h * 0.3))

        login_select = Button('text', None, None, None, None, 'Login', Font(30), '#676f9d', '#5d648c', (size.w * 0.265, size.h * 0.178))
        signup_select = Draw_Screen('text', None, None, None, None, 'Sign up', Font(30), '#f9b17a',(size.w * 0.35, size.h * 0.178))

        username_form = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None)
        password_form = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None)

        username_form_text = Draw_Screen('text', None, None, None, None, 'username', Font(20), '#424769', (size.w * 0.22, size.h * 0.41))
        password_form_text = Draw_Screen('text', None, None, None, None, 'password', Font(20), '#424769', (size.w * 0.22, size.h * 0.54))

        forgot_password = Button('text', None, None, None, None, 'Forgor password?', Font(20), '#676f9d', '#d69869', (size.w * 0.405, size.h * 0.64))

        Login_Button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None)
        FaceID_Button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None)

        Login_Button_text = Draw_Screen('text', None, None, None, None, 'Login', Font(30), '#424769', (size.w * 0.225, size.h * 0.73))
        FaceID_Button_text = Draw_Screen('text', None, None, None, None, 'Face ID', Font(30), '#424769', (size.w * 0.395, size.h * 0.73))

        screen.fill('#2d3250')
        bg.Blit()
        menu.Blit()

        login_select.Blit()
        signup_select.Blit()
        welcome_text.Blit()

        username_form.Blit()
        password_form.Blit()
        forgot_password.Blit()
        Login_Button.Blit()
        FaceID_Button.Blit()

        for button in [login_select, username_form, password_form, Login_Button, FaceID_Button]:
            button.Change_Color(mouse_pos)
        
        username_form_text.Blit()
        password_form_text.Blit()
        Login_Button_text.Blit()
        FaceID_Button_text.Blit()

        
        #pg.draw.line(screen, "White", (0, size.h/2), (size.w, size.h/2))
        #pg.draw.line(screen, "White", (size.w * 0.3125, 0), (size.w * 0.312, size.h))
        
        pg.time.Clock().tick(120)
        pg.display.update()

#def Start_Menu():
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
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Login_Page()
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

#def Options():
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