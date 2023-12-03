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

    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))

    welcome = Font(int(80 * size.w / 1280)).render('Welcome', True, '#ffffff')

    login_select = Font(int(30 * size.w / 1280)).render('Login', True, '#d69869')
    signup_select = Button('text', None, None, None, None, 'Sign up', Font(int(30 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.35, size.h * 0.178))

    username_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    username_box_text = Font(int(20 * size.w / 1280)).render('username', True, '#424769')
    password_box_text = Font(int(20 * size.w / 1280)).render('password', True, '#424769')

    forgot_password = Button('text', None, None, None, None, 'Forgor password?', Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.405, size.h * 0.64))

    Login_Button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)
    FaceID_Button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)

    Login_Button_text = Font(int(30 * size.w / 1280)).render('Login', True, '#424769')
    FaceID_Button_text = Font(int(30 * size.w / 1280)).render('Face ID', True, '#424769')

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
                    Title_Screen()
                if (signup_select.Mouse_Click(mouse_pos)):
                    Signup_Page()
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        screen.fill('#2d3250')
        screen.blit(bg, (size.w*0.125, size.h*0.125))
        pg.draw.rect(screen, '#424769', [size.w*0.125, size.h*0.125, size.w*0.375, size.h * 0.75])

        signup_select.Blit()
        username_box.Blit()
        password_box.Blit()
        forgot_password.Blit()
        Login_Button.Blit()
        FaceID_Button.Blit()

        for button in [signup_select, username_box, password_box, Login_Button, FaceID_Button, forgot_password]:
            button.Change_Color(mouse_pos)
        
        screen.blit(login_select      ,   login_select.get_rect(center = (size.w * 0.265, size.h * 0.178)))
        screen.blit(welcome           ,   welcome.get_rect(center = (size.w * 0.3125, size.h * 0.3)))
        screen.blit(username_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.41)))
        screen.blit(password_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.54)))
        screen.blit(Login_Button_text ,   Login_Button_text.get_rect(center = (Login_Button.rect.center)))
        screen.blit(FaceID_Button_text,   FaceID_Button_text.get_rect(center = (FaceID_Button.rect.center)))

        mouse_animation.update()
        mouse_animation.draw(screen)
        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
        #pg.draw.line(screen, "White", (0, size.h/2), (size.w, size.h/2))
        #pg.draw.line(screen, "White", (size.w * 0.3125, 0), (size.w * 0.312, size.h))
        
        pg.time.Clock().tick(60)
        pg.display.update()

def Signup_Page():
    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))

    welcome = Font(int(80 * size.w / 1280)).render('Welcome', True, '#ffffff')

    login_select = Button('text', None, None, None, None, 'Login', Font(int(30 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.265, size.h * 0.178))
    signup_select = Font(int(30 * size.w / 1280)).render('Sign up', True, '#d69869')

    username_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    username_box_text = Font(int(20 * size.w / 1280)).render('username', True, '#424769')
    password_box_text = Font(int(20 * size.w / 1280)).render('password', True, '#424769')

    forgot_password = Button('text', None, None, None, None, 'Forgor password?', Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.405, size.h * 0.64))

    Login_Button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)
    FaceID_Button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)

    Login_Button_text = Font(int(30 * size.w / 1280)).render('Login', True, '#424769')
    FaceID_Button_text = Font(int(30 * size.w / 1280)).render('Face ID', True, '#424769')
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
        screen.blit(bg, (size.w*0.125, size.h*0.125))
        pg.draw.rect(screen, '#424769', [size.w*0.125, size.h*0.125, size.w*0.375, size.h * 0.75])

        login_select.Blit()
        username_box.Blit()
        password_box.Blit()
        forgot_password.Blit()
        Login_Button.Blit()
        FaceID_Button.Blit()

        for button in [login_select, username_box, password_box, Login_Button, FaceID_Button, forgot_password]:
            button.Change_Color(mouse_pos)

        screen.blit(signup_select     ,   signup_select.get_rect(center = (size.w * 0.35, size.h * 0.178)))
        screen.blit(welcome           ,   welcome.get_rect(center = (size.w * 0.3125, size.h * 0.3)))
        screen.blit(username_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.41)))
        screen.blit(password_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.54)))
        screen.blit(Login_Button_text ,   Login_Button_text.get_rect(center = (Login_Button.rect.center)))
        screen.blit(FaceID_Button_text,   FaceID_Button_text.get_rect(center = (FaceID_Button.rect.center)))

        mouse_animation.update()
        mouse_animation.draw(screen)
        #pg.draw.line(screen, "White", (0, size.h/2), (size.w, size.h/2))
        #pg.draw.line(screen, "White", (size.w * 0.3125, 0), (size.w * 0.312, size.h))
        
        pg.time.Clock().tick(60)
        pg.display.update()

def Title_Screen():
    Title_Loop = 0
    alpha = 0
    enter_game = False
    fps = 0
    tru_fps = 0

    Background = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert_alpha(), (size.w*1.15, size.h*1.15))
        
    Quit = Button('image', None, None, 'Assets/icon/Settings/shut_down01.png', (60*size.w/1280, 60* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shut_down02.png', (size.w * 0.03, size.h * 0.95))

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting02.png', (size.w * 0.97, size.h * 0.05))
    
    Title = Draw_Screen('text', None, None, None, None, 'Racing Bet', 
                    Font(int(150 * size.w / 1280)), '#000000', (size.w * 0.5, size.h *(0.25 + 0.04 * sin(Title_Loop))))
        
    Prompt = Draw_Screen('text', None, None, None, None, '- Click anywhere to enter -', 
                    Font(int(40 * size.w / 1280)), '#000000', (size.w * 0.5, size.h * 0.75))
    while True:
        alpha += 7.5
        fps += 1
        Title_Loop += 0.1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Quit.Mouse_Click(mouse_pos) == True and enter_game == False:
                    pg.quit()
                    sys.exit()
                if (Settings.Mouse_Click(mouse_pos) == True and enter_game == False):
                    pg.image.save(screen, 'Assets/temps/temp.png')
                    Video_Setting('Start Menu')
                else:
                    enter_game = True
                    alpha = 255

            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0
        

        Bg = Dynamic_Background(Background, (size.w / 2, size.h / 2), mouse_pos)

        screen.fill(0)
        Background.set_alpha(alpha)
        Title.text.set_alpha(alpha)
        Prompt.text.set_alpha(255 * abs(sin(rad(alpha))))
        Bg.Draw()

        Title.Blit()
        Prompt.Blit()
        Quit.Blit()
        Settings.Blit()

        if enter_game:
            alpha -= 15
            if alpha < 0:
                In_Game_Menu(0)
        else:
            for button in [Quit, Settings]:
                button.Change_Color(mouse_pos)
        
        mouse_animation.update()
        mouse_animation.draw(screen)

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))



        pg.time.Clock().tick(60)
        pg.display.update()

def Video_Setting(prev_menu):
    change_size = True
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
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
                if Return.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Title_Screen()
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(0)
                if Full_Screen.Mouse_Click(mouse_pos):
                    size.Full_Screen()
                if _1366x768.Mouse_Click(mouse_pos):
                    size.Window((1366, 768))
                if _1280x720.Mouse_Click(mouse_pos):
                    size.Window((1280, 720))    
            if event.type == pg.WINDOWSIZECHANGED:
                change_size = True

        if change_size:
            bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))

            Video = Draw_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
            Video_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(int(40 * size.w / 1280)), '#424769', Video.rect.center)

            Audio = Button('rect', Video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(int(40 * size.w / 1280)), '#424769', Audio.rect.center)

            Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(int(40 * size.w / 1280)), '#424769', Language.rect.center)

            User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(int(40 * size.w / 1280)), '#424769', User_Center.rect.center)

            Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            Return_text = Draw_Screen('text', None, None, None, None, 'Return', Font(int(40 * size.w / 1280)), '#424769', Return.rect.center)

            Full_Screen = Button('rect', (size.w * 0.325, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            Full_Screen_text = Font(int(40 * size.w / 1280)).render('Full Screen', True, '#424769')

            _1366x768 = Button('rect', (size.w * 0.5125, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            _1366x768_text = Font(int(40 * size.w / 1280)).render('1366 x 768', True, '#424769')

            _1280x720 = Button('rect', (size.w * 0.7, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            _1280x720_text = Font(int(40 * size.w / 1280)).render('1280 x 720', True, '#424769')

        change_size = False
        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        Video.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Return.Blit()

        Full_Screen.Blit()
        _1366x768.Blit()
        _1280x720.Blit()

        for button in [Full_Screen, _1366x768, _1280x720, Audio, Language, User_Center, Return]:
            button.Change_Color(mouse_pos)

        Video_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Return_text.Blit()

        screen.blit(Full_Screen_text, Full_Screen_text.get_rect(center = (Full_Screen.rect.center)))
        screen.blit(_1366x768_text, Full_Screen_text.get_rect(center = (_1366x768.rect.center)))
        screen.blit(_1280x720_text, Full_Screen_text.get_rect(center = (_1280x720.rect.center)))

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Audio_Setting(prev_menu):
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))

    Graphics = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(int(40* size.w / 1280)), '#424769', Graphics.rect.center)

    Audio = Draw_Screen('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(int(40* size.w / 1280)), '#424769', Audio.rect.center)

    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(int(40* size.w / 1280)), '#424769', Language.rect.center)

    User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(int(40* size.w / 1280)), '#424769', User_Center.rect.center)

    Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Return_text = Draw_Screen('text', None, None, None, None, 'Return', Font(int(40* size.w / 1280)), '#424769', Return.rect.center)
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
                if Return.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Title_Screen()
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(0)

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Return.Blit()


        for button in [Graphics, Language, User_Center, Return]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Return_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Language_Setting(prev_menu):
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))

    Graphics = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(40), '#424769', Graphics.rect.center)

    Audio = Button('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d','#5d648c', None, None)
    Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(40), '#424769', Audio.rect.center)

    Language = Draw_Screen('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(40), '#424769', Language.rect.center)

    User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(40), '#424769', User_Center.rect.center)

    Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Return_text = Draw_Screen('text', None, None, None, None, 'Return', Font(40), '#424769', Return.rect.center)
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
                if Return.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Title_Screen()
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(0)

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])
        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Return.Blit()

        for button in [Graphics, Audio, User_Center, Return]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Return_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)


        pg.display.update()
        pg.time.Clock().tick(60)

def User_Center_Setting(prev_menu):
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))

    Graphics = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Graphics_text = Draw_Screen('text', None, None, None, None, 'Graphics', Font(40), '#424769', Graphics.rect.center)

    Audio = Button('rect', Graphics.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Audio_text = Draw_Screen('text', None, None, None, None, 'Audio', Font(40), '#424769', Audio.rect.center)

    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Language_text = Draw_Screen('text', None, None, None, None, 'Language', Font(40), '#424769', Language.rect.center)

    User_Center = Draw_Screen('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    User_Center_text = Draw_Screen('text', None, None, None, None, 'User Center', Font(40), '#424769', User_Center.rect.center)

    Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Return_text = Draw_Screen('text', None, None, None, None, 'Return', Font(40), '#424769', Return.rect.center)

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
                if Return.Mouse_Click(mouse_pos):
                    if prev_menu == 'Start Menu':
                        Title_Screen()
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(0)

        
        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        Graphics.Blit()
        Audio.Blit()
        Language.Blit()
        User_Center.Blit()
        Return.Blit()

        for button in [Graphics, Audio, Language, Return]:
            button.Change_Color(mouse_pos)

        Graphics_text.Blit()
        Audio_text.Blit()
        Language_text.Blit()
        User_Center_text.Blit()
        Return_text.Blit()

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def In_Game_Menu(alpha):
    Change_Menu = False
    Target_Menu = ''
    fps = 0
    tru_fps = 0
    Background = pg.transform.scale(pg.image.load('Assets/icon/Settings/Cafe.png').convert_alpha(), (512, 288))
    Background = pg.transform.smoothscale(Background, (size.w*1.15, size.h*1.15))

    Money_Gone = pg.transform.scale(pg.image.load('Assets/icon/Settings/Money_Gone.png').convert_alpha(), (128, 72))
    Money_Gone = pg.transform.scale(Money_Gone, (size.w * 0.4, size.h * 0.4))

    User_Info_Tab = pg.Surface((size.w, size.h * 0.1), pg.SRCALPHA)
    User_Info_Tab.fill('#2d3250')

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting02.png', (size.w * 0.97, size.h * 0.05))

    Play = Button('image', None, None, 'Assets/icon/Settings/Play.png', (size.w*0.3, size.h * 0.2), None, None, None, None, 'Assets/icon/Settings/Play_Hover.png', (size.w*0.775, size.h * 0.3))
    Play_Break = pg.transform.scale(pg.image.load('Assets/icon/Settings/Play_Break.png').convert_alpha(), (size.w*0.3, size.h * 0.2))

    Mini_Game = Button('image', None, None, 'Assets/icon/Settings/Mini Game.png', (size.w*0.3, size.h * 0.2), None, None, None, None, 'Assets/icon/Settings/Mini Game Hover.png', (size.w*0.775, size.h * 0.55))
    Mini_Game_CLick = pg.transform.scale(pg.image.load('Assets/icon/Settings/Mini Game Click.png').convert_alpha(), (size.w*0.3, size.h * 0.2))

    Rank = Button('image', None, None, 'Assets/icon/Settings/Rank.png', (size.w*0.3, size.h * 0.2), None, None, None, None, 'Assets/icon/Settings/Rank Hover.png', (size.w*0.775, size.h * 0.8))
    Rank_Click = pg.transform.scale(pg.image.load('Assets/icon/Settings/Rank Click.png').convert_alpha(), (size.w*0.3, size.h * 0.2))
    while True:
        alpha += 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Change_Menu == False:
                    if Play.Mouse_Click(mouse_pos):
                        Change_Menu = True
                        Target_Menu = 'Play'
                        alpha = 255
                    if Mini_Game.Mouse_Click(mouse_pos):
                        Change_Menu = True
                        Target_Menu = 'Mini Game'
                        alpha = 255
                    if Rank.Mouse_Click(mouse_pos):
                        Change_Menu = True
                        Target_Menu = 'Rank'
                        alpha = 255
                    if Settings.Mouse_Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Setting('In_Game_Menu')

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Title_Screen()
            
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        screen.fill(0)
        Bg = Dynamic_Background(Background, (size.w / 2, size.h / 2), mouse_pos)
        if alpha <= 255:
            for stuff in [Background, Money_Gone, Play_Break, Play.image, Mini_Game.image, 
                          Mini_Game_CLick, Rank.image, Rank_Click, User_Info_Tab]:
                stuff.set_alpha(alpha)

        Bg.Draw()
        
        screen.blit(Money_Gone, Money_Gone.get_rect(center = (size.w * 0.25, size.h * 0.55)))
        screen.blit(User_Info_Tab, (0,0))

        Play.Blit()
        Mini_Game.Blit()
        Rank.Blit()
        Settings.Blit()

        if Change_Menu:
            alpha -= 15
            if Target_Menu == 'Play':
                screen.blit(Play_Break, Play_Break.get_rect(center = (Play.rect.center)))
                if alpha < 0:
                    Choose_Character_Set(0)
            elif Target_Menu == 'Mini Game':
                screen.blit(Mini_Game_CLick, Mini_Game_CLick.get_rect(center = (Mini_Game.rect.center)))
                if alpha < 0:
                    pass
            elif Target_Menu == 'Rank':
                screen.blit(Rank_Click, Rank_Click.get_rect(center = (Rank.rect.center)))
                if alpha < 0:
                    pass
        elif alpha > 225 and Change_Menu == False:
            for button in [Settings, Play, Mini_Game, Rank]:
                button.Change_Color(mouse_pos)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

def Choose_Character_Set(alpha):
    Change_Menu = False
    Target_Menu = ''
    fps = 0
    tru_fps = 0
    Background = pg.transform.scale(pg.image.load('Assets/icon/Settings/Cafe.png').convert_alpha(), (512, 288))
    Background = pg.transform.smoothscale(Background, (size.w*1.15, size.h*1.15))

    User_Info_Tab = pg.Surface((size.w, size.h * 0.1), pg.SRCALPHA)
    User_Info_Tab.fill('#2d3250')

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting02.png', (size.w * 0.97, size.h * 0.05))
    
    Continue = Button('image', None, None, 'Assets/icon/Settings/Continue.png', (60*size.w/1280, 60* size.w/1280), None, None, None, None, 'Assets/icon/Settings/Continue.png', (size.w*0.025, size.h * 0.95))

    Return = Button('image', None, None, 'Assets/icon/Settings/Return.png', (60*size.w/1280, 60* size.w/1280), None, None, None, None, 'Assets/icon/Settings/Return.png', (size.w*0.975, size.h * 0.95))
    while True:
        alpha += 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Mouse_Animation(mouse_pos, 5, size.w))
                if Change_Menu == False:
                    if Settings.Mouse_Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Setting('Choose_Character_Set')

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                Title_Screen()
            
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        screen.fill(0)
        Bg = Dynamic_Background(Background, (size.w / 2, size.h / 2), mouse_pos)
        if alpha <= 255:
            for stuff in [Background, User_Info_Tab, Return.image, Continue.image]:
                stuff.set_alpha(alpha)

        Bg.Draw()

        screen.blit(User_Info_Tab, (0,0))
        Settings.Blit()
        Return.Blit()
        Continue.Blit()

        if Change_Menu:
            pass
        elif alpha > 225 and Change_Menu == False:
            for button in [Settings, Continue, Return]:
                button.Change_Color(mouse_pos)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

Start_Animation()
