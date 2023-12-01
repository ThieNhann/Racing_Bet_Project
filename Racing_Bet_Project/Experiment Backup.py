import pygame as pg
import sys
import os
from math import sin, radians as rad
from Experiment_Class import *


pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '0'
pg.display.set_caption("Racing Bet")
size = Screen_Info(screen.get_size())
mouse_animation = pg.sprite.Group()
Bg_cycle = pg.USEREVENT + 1
pg.time.set_timer(Bg_cycle, 1000)

def Start_Animation():
    alpha = 250
    while True:
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

        alpha += 1.75
        if alpha < 180 and alpha > 0:
            logo.set_alpha(int(255 * sin(rad(alpha))))
            screen.blit(logo, logo_rect)
        elif alpha > 250:
            mouse_animation.empty()
            Login_Page()


        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

def Login_Page():
    fps = 0
    tru_fps = 0

    bg = Draw_Screen('image', None, None, 'Assets/background/village/village.png', (size.w*0.75, size.h*0.75), None, None, None, (size.w*0.5, size.h*0.5))
    menu = Draw_Screen('rect', bg.rect.topleft, (size.w*0.375, size.h * 0.75), None, None, None, None, '#424769', None)

    welcome_text = Draw_Screen('text', None, None, None, None, 'Welcome', Font(80), '#ffffff', (size.w * 0.3125, size.h * 0.3))

    login_select = Draw_Screen('text', None, None, None, None, 'Login', Font(30), '#f9b17a', (size.w * 0.265, size.h * 0.178))
    signup_select = Button('text', None, None, None, None, 'Sign up', Font(30), '#676f9d', '#5d648c', None, (size.w * 0.35, size.h * 0.178))

    username_form = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_form = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    username_form_text = Draw_Screen('text', None, None, None, None, 'username', Font(20), '#424769', (size.w * 0.22, size.h * 0.41))
    password_form_text = Draw_Screen('text', None, None, None, None, 'password', Font(20), '#424769', (size.w * 0.22, size.h * 0.54))

    forgot_password = Button('text', None, None, None, None, 'Forgor password?', Font(20), '#676f9d', '#d69869', None, (size.w * 0.405, size.h * 0.64))

    Login_Button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)
    FaceID_Button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)

    Login_Button_text = Draw_Screen('text', None, None, None, None, 'Login', Font(30), '#424769', (size.w * 0.225, size.h * 0.73))
    FaceID_Button_text = Draw_Screen('text', None, None, None, None, 'Face ID', Font(30), '#424769', (size.w * 0.395, size.h * 0.73))

    while True:
        mouse_pos = pg.mouse.get_pos()
        fps += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                #Start_Menu()
                pass
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if (Login_Button.Mouse_Click(mouse_pos)):
                    Start_Menu()
                if (signup_select.Mouse_Click(mouse_pos)):
                    Signup_Page()
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

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

        mouse_animation.update()
        mouse_animation.draw(screen)
        FPS = Font(30).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
        #pg.draw.line(screen, "White", (0, size.h/2), (size.w, size.h/2))
        #pg.draw.line(screen, "White", (size.w * 0.3125, 0), (size.w * 0.312, size.h))
        
        pg.time.Clock().tick(60)
        pg.display.update()

def Signup_Page():
    bg = Draw_Screen('image', None, None, 'Assets/background/village/village.png', (size.w*0.75, size.h*0.75), None, None, None, (size.w*0.5, size.h*0.5))
    menu = Draw_Screen('rect', bg.rect.topleft, (size.w*0.375, size.h * 0.75), None, None, None, None, '#424769', None)

    welcome_text = Draw_Screen('text', None, None, None, None, 'Welcome', Font(80), '#ffffff', (size.w * 0.3125, size.h * 0.3))

    login_select = Button('text', None, None, None, None, 'Login', Font(30), '#676f9d', '#5d648c', None, (size.w * 0.265, size.h * 0.178))
    signup_select = Draw_Screen('text', None, None, None, None, 'Sign up', Font(30), '#f9b17a',(size.w * 0.35, size.h * 0.178))

    username_form = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_form = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    username_form_text = Draw_Screen('text', None, None, None, None, 'username', Font(20), '#424769', (size.w * 0.22, size.h * 0.41))
    password_form_text = Draw_Screen('text', None, None, None, None, 'password', Font(20), '#424769', (size.w * 0.22, size.h * 0.54))

    forgot_password = Button('text', None, None, None, None, 'Forgor password?', Font(20), '#676f9d', '#d69869', None, (size.w * 0.405, size.h * 0.64))

    Login_Button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None, None)
    FaceID_Button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None, None)

    Login_Button_text = Draw_Screen('text', None, None, None, None, 'Login', Font(30), '#424769', (size.w * 0.225, size.h * 0.73))
    FaceID_Button_text = Draw_Screen('text', None, None, None, None, 'Face ID', Font(30), '#424769', (size.w * 0.395, size.h * 0.73))
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
                if (Login_Button.Mouse_Click(mouse_pos)):
                    print("Spooky")
                if(login_select.Mouse_Click(mouse_pos)):
                    Login_Page()


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

        mouse_animation.update()
        mouse_animation.draw(screen)
        #pg.draw.line(screen, "White", (0, size.h/2), (size.w, size.h/2))
        #pg.draw.line(screen, "White", (size.w * 0.3125, 0), (size.w * 0.312, size.h))
        
        pg.time.Clock().tick(60)
        pg.display.update()

def Start_Menu():
    Title_Loop = 0
    alpha = 0
    fps = 0
    tru_fps = 0

    Background = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert_alpha(), (size.w*1.15, size.h*1.15))
        
    Quit = Button('image', None, None, 'Assets/icon/Settings/shut_down01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/shut_down02.png', (size.w * 0.03, size.h * 0.95))

    User_Icon = Button('image', None, None, 'Assets/icon/Settings/user_icon01.png', (60*size.w/1280, 60* size.w/1280), 
                        None, None, None, None, 'Assets/icon/Settings/user_icon02.png', (size.w * 0.97, size.h * 0.05))

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting01.png', (60*size.w/1280, 60* size.w/1280), 
                        None, None, None, None, 'Assets/icon/Settings/setting02.png', (size.w * 0.97, size.h * 0.15))
    
    while True:
        alpha += 5
        fps += 1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Quit.Mouse_Click(mouse_pos):
                    pg.quit()
                    sys.exit()
                if (Settings.Mouse_Click(mouse_pos)):
                    Setting_Page('Start Menu')
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Login_Page()


            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0
        
        Title_Loop += 0.1

        Bg = Dynamic_Background(Background, (size.w / 2, size.h / 2), mouse_pos)
        Title = Draw_Screen('text', None, None, None, None, 'Racing Bet', 
                            Font(int(150 * size.w / 1280)), '#000000', (size.w * 0.5, size.h *(0.25 + 0.04 * sin(Title_Loop))))
        
        Prompt = Draw_Screen('text', None, None, None, None, '- Click anywhere to enter -', 
                            Font(int(40 * size.w / 1280)), '#000000', (size.w * 0.5, size.h * 0.75))
        
        

        Background.set_alpha(alpha)
        Title.text.set_alpha(alpha)
        Prompt.text.set_alpha(255 * abs(sin(rad(alpha))))
        Bg.Draw()

        Title.Blit()
        Prompt.Blit()
        Quit.Blit()
        User_Icon.Blit()
        Settings.Blit()

        for button in [Quit, User_Icon, Settings]:
            button.Change_Color(mouse_pos)
        
        mouse_animation.update()
        mouse_animation.draw(screen)

        FPS = Font(30).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))

        pg.time.Clock().tick(60)
        pg.display.update()

def Setting_Page(prev_menu):
    bg = pg.transform.smoothscale(pg.image.load('Assets/background/village/village.png').convert(), (128*3, 72*3))
    bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))
    menu = Draw_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.75, size.h * 0.75), None, None, None, None, '#2d3250', None)
    setting_option = Draw_Screen('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.75), None, None, None, None, '#676f9d', None)

    Graphics = Button('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(40), '#424769', Graphics.rect.center)

    Audio = Button('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(40), '#424769', Audio.rect.center)

    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(40), '#424769', Language.rect.center)

    User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(40), '#424769', User_Center.rect.center)

    Exit = Button('rect', (menu.rect.bottomleft[0], menu.rect.bottomleft[1] - size.h * 0.1), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Exit_text = Draw_Screen('text', None, None, None, None, 'Exit', Font(40), '#424769', Exit.rect.center)

    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Graphics.Mouse_Click(mouse_pos):
                    Video_Setting(prev_menu)
                if Audio.Mouse_Click(mouse_pos):
                    Audio_Setting(prev_menu)
                if Language.Mouse_Click(mouse_pos):
                    Language_Setting(prev_menu)
                if User_Center.Mouse_Click(mouse_pos):
                    User_Center_Setting(prev_menu)
                if Exit.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Start_Menu()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Start_Menu()

        screen.blit(bg, (0,0))
        menu.Blit()
        setting_option.Blit()
        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Exit.Blit()

        for button in [Graphics, Audio, Language, User_Center, Exit]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Exit_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Video_Setting(prev_menu):
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Audio.Mouse_Click(mouse_pos):
                    Audio_Setting(prev_menu)
                if Language.Mouse_Click(mouse_pos):
                    Language_Setting(prev_menu)
                if User_Center.Mouse_Click(mouse_pos):
                    User_Center_Setting(prev_menu)
                if Exit.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Start_Menu()
                if Full_Screen.Mouse_Click(mouse_pos):
                    size.Full_Screen()
                if _1280x720.Mouse_Click(mouse_pos):
                    size.Window((1280, 720))
                if _800x600.Mouse_Click(mouse_pos):
                    size.Window((800, 600))
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Setting_Page()


        bg = pg.transform.smoothscale(pg.image.load('Assets/background/village/village.png').convert(), (128*3, 72*3))
        bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))
        menu = Draw_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.75, size.h * 0.75), None, None, None, None, '#2d3250', None)
        setting_option = Draw_Screen('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.75), None, None, None, None, '#676f9d', None)

        Graphics = Draw_Screen('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
        Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(40), '#424769', Graphics.rect.center)

        Audio = Button('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
        Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(40), '#424769', Audio.rect.center)

        Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
        Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(40), '#424769', Language.rect.center)

        User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
        User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(40), '#424769', User_Center.rect.center)

        Exit = Button('rect', (menu.rect.bottomleft[0], menu.rect.bottomleft[1] - size.h * 0.1), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
        Exit_text = Draw_Screen('text', None, None, None, None, 'Exit', Font(40), '#424769', Exit.rect.center)

        Full_Screen = Button('rect', (size.w * 0.325, size.h * 0.225), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
        Full_Screen_text = Draw_Screen('text', None, None, None, None, 'Full_Screen', Font(40), '#424769', Full_Screen.rect.center)
        _1280x720 = Button('rect', (size.w * 0.5, size.h * 0.225), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
        _1280x720_text = Draw_Screen('text', None, None, None, None, '1280 x 720', Font(40), '#424769', _1280x720.rect.center)
        _800x600 = Button('rect', (size.w * 0.675, size.h * 0.225), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
        _800x600_text = Draw_Screen('text', None, None, None, None, '800 x 600', Font(40), '#424769', _800x600.rect.center)

        screen.blit(bg, (0,0))
        menu.Blit()
        setting_option.Blit()
        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Exit.Blit()

        Full_Screen.Blit()
        _1280x720.Blit()
        _800x600.Blit()

        for button in [Full_Screen, _1280x720, _800x600, Audio, Language, User_Center, Exit]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Exit_text.Blit()

        Full_Screen_text.Blit()
        _1280x720_text.Blit()
        _800x600_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(90)

def Audio_Setting(prev_menu):
    bg = pg.transform.smoothscale(pg.image.load('Assets/background/village/village.png').convert(), (128*3, 72*3))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))
    menu = Draw_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.75, size.h * 0.75), None, None, None, None, '#2d3250', None)
    setting_option = Draw_Screen('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.75), None, None, None, None, '#676f9d', None)

    Graphics = Button('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(40), '#424769', Graphics.rect.center)

    Audio = Draw_Screen('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(40), '#424769', Audio.rect.center)

    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(40), '#424769', Language.rect.center)

    User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(40), '#424769', User_Center.rect.center)

    Exit = Button('rect', (menu.rect.bottomleft[0], menu.rect.bottomleft[1] - size.h * 0.1), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Exit_text = Draw_Screen('text', None, None, None, None, 'Exit', Font(40), '#424769', Exit.rect.center)
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Graphics.Mouse_Click(mouse_pos):
                    Video_Setting(prev_menu)
                if Language.Mouse_Click(mouse_pos):
                    Language_Setting(prev_menu)
                if User_Center.Mouse_Click(mouse_pos):
                    User_Center_Setting(prev_menu)
                if Exit.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Start_Menu()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Setting_Page()

        

        screen.blit(bg, (0,0))
        menu.Blit()
        setting_option.Blit()
        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Exit.Blit()


        for button in [Graphics, Language, User_Center, Exit]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Exit_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Language_Setting(prev_menu):
    bg = pg.transform.smoothscale(pg.image.load('Assets/background/village/village.png').convert(), (128*3, 72*3))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))
    menu = Draw_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.75, size.h * 0.75), None, None, None, None, '#2d3250', None)
    setting_option = Draw_Screen('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.75), None, None, None, None, '#676f9d', None)

    Graphics = Button('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(40), '#424769', Graphics.rect.center)

    Audio = Button('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d','#f9b17a', None, None)
    Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(40), '#424769', Audio.rect.center)

    Language = Draw_Screen('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(40), '#424769', Language.rect.center)

    User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(40), '#424769', User_Center.rect.center)

    Exit = Button('rect', (menu.rect.bottomleft[0], menu.rect.bottomleft[1] - size.h * 0.1), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Exit_text = Draw_Screen('text', None, None, None, None, 'Exit', Font(40), '#424769', Exit.rect.center)
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Graphics.Mouse_Click(mouse_pos):
                    Video_Setting(prev_menu)
                if Audio.Mouse_Click(mouse_pos):
                    Audio_Setting(prev_menu)
                if User_Center.Mouse_Click(mouse_pos):
                    User_Center_Setting(prev_menu)
                if Exit.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Start_Menu()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Setting_Page()

        screen.blit(bg, (0,0))
        menu.Blit()
        setting_option.Blit()
        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Exit.Blit()

        for button in [Graphics, Audio, User_Center, Exit]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Exit_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)


        pg.display.update()
        pg.time.Clock().tick(60)

def User_Center_Setting(prev_menu):
    bg = pg.transform.smoothscale(pg.image.load('Assets/background/village/village.png').convert(), (128*3, 72*3))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))
    menu = Draw_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.75, size.h * 0.75), None, None, None, None, '#2d3250', None)
    setting_option = Draw_Screen('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.75), None, None, None, None, '#676f9d', None)

    Graphics = Button('rect', menu.rect.topleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(40), '#424769', Graphics.rect.center)

    Audio = Button('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(40), '#424769', Audio.rect.center)

    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(40), '#424769', Language.rect.center)

    User_Center = Draw_Screen('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(40), '#424769', User_Center.rect.center)

    Exit = Button('rect', (menu.rect.bottomleft[0], menu.rect.bottomleft[1] - size.h * 0.1), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Exit_text = Draw_Screen('text', None, None, None, None, 'Exit', Font(40), '#424769', Exit.rect.center)
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Graphics.Mouse_Click(mouse_pos):
                    Video_Setting(prev_menu)
                if Audio.Mouse_Click(mouse_pos):
                    Audio_Setting(prev_menu)
                if Language.Mouse_Click(mouse_pos):
                    Language_Setting(prev_menu)
                if Exit.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Start_Menu()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Setting_Page()

        
        screen.blit(bg, (0,0))
        menu.Blit()
        setting_option.Blit()
        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Exit.Blit()

        for button in [Graphics, Audio, Language, Exit]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Exit_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

Start_Animation()
