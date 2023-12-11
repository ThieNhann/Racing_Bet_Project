import pygame as pg
import json
import sys
import os
from email_validator import validate_email
import smtplib
import ssl
from email.message import EmailMessage
from math import sin, radians as rad
from Experiment_Class import *
from random import randint, randrange

#You may wonder why i didn't use pygame_menu and yes im asking the same question rn but eh too late
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '0'
pg.display.set_caption("Racing Bet")

#music playback
pg.mixer.init(48000, -16, 4)

music_channels = pg.mixer.Channel(1)
sfx_channels = pg.mixer.Channel(2)

title_music = pg.mixer.Sound('Assets/music/Forest (rushed ver).wav')
button_click = pg.mixer.Sound('Assets/menu_click.mp3')
interface = pg.mixer.Sound('Assets/interface.mp3')

#Mainly for deleting info when backspace is held
pg.key.set_repeat(600, 25)

#size of current screen
size = Screen_Info(screen.get_size())

#mouse animation group
mouse_animation = pg.sprite.Group()

#FPS event counter
Bg_cycle = pg.USEREVENT + 1
pg.time.set_timer(Bg_cycle, 1000)

#Load the config (lang, volume)
def Load_Config():
    global US, VN, lang, music_volume, sfx_volume

    #open config files
    with open('locale/en_US.json', 'r', encoding="utf8") as f:
        US = json.load(f)
    with open('locale/vi_VN.json', 'r', encoding="utf8") as f:
        VN = json.load(f)

    #if config file not available then set default
    try:
        with open ('settings/Config.json', 'r') as f:
            config = json.load(f)
            lang = config['Start_Language']
            music_volume = float(config['Music_Volume'])
            sfx_volume = float(config['SFX_Volume'])
    except:
        lang = 'US'
        music_volume = 1.0
        sfx_volume = 1.0
    

    sfx_channels.set_volume(sfx_volume)
    music_channels.set_volume(music_volume)

#Save config when shutdown
def Shutdown():

    #write to config file
    save_config = {"Start_Language"     : f"{lang}", 
                   "Start_Screen_Size"  : f"{screen.get_size()}",
                   "In_Full_Screen"     : f"{in_full_screen}",
                    "Music_Volume"      : f"{music_volume}",
                    "SFX_Volume"        : f"{sfx_volume}"
                  }
    
    json_file = json.dumps(save_config, indent = 4)
    with open ('settings/config.json', 'w') as f:
        f.write(json_file)

    pg.quit()
    sys.exit()

#Update text when lang changed
def Updt_Lang(lang, menu, name):

    if (lang == 'US')   :  return(f'{US[menu][name]}')
    elif (lang == 'VN') :  return(f'{VN[menu][name]}')
        
#Validate the email
def Validate_Email(email):
    try:
        validate_email(email)
        return True
    except:
        return False

#Send confirmation code
def Send_Email(username):
    #Get password (private reason ehe)
    with open ("C:/Users/ADMIN/Desktop/app.txt", 'r') as f:
        password = f.read()
    
    #Get sender and receiver
    sender = "mihikoxakamatsu@gmail.com"
    receiver = username

    #Generate code
    code = randint(100000, 999999)

    #Email content
    Title = "Email Verifications for School Project"
    Body = f"""
    Your email verification code is: {code}
        
    Please ignore this email if it is mistakenly sent to you."""
    
    #Encode
    code = hashlib.sha256(password.encode()).hexdigest()

    #Making the emails
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = Title
    em.set_content(Body)

    context = ssl.create_default_context()

    #Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())

    #return to compare with user input
    return code

#Settings tab
def Video_Menu(prev_menu, set_char, race_length):
    global in_full_screen

    #Update everything only once to improve performance
    change_size = True

    #Set the image of the previous menu as background
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))

    while True:

        #Position of the mouse
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to different setting menus
                if Audio.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Menu(prev_menu, set_char, race_length)

                if Language.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Menu(prev_menu, set_char, race_length)

                if User_Center.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Menu(prev_menu, set_char, race_length)

                #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Start Menu':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_length)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_length)
                
                #Change resolutions
                if Full_Screen.Mouse_Click(mouse_pos):
                    sfx_channels.play(interface)
                    in_full_screen = True
                    size.Full_Screen()

                if _1366x768.Mouse_Click(mouse_pos):
                    sfx_channels.play(interface)
                    in_full_screen = False
                    size.Window((1366, 768))

                if _1280x720.Mouse_Click(mouse_pos):
                    sfx_channels.play(interface)
                    in_full_screen = False
                    size.Window((1280, 720))    

            #Update everything within the menu when size changed
            if event.type == pg.WINDOWSIZECHANGED:
                change_size = True

        #If a size change is detected, create new object that replace the old one with new resolution
        if change_size:

            bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))

            Video = Draw_to_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
            Audio = Button('rect', Video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

            Full_Screen = Button('rect', (size.w * 0.325, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            _1366x768 = Button('rect', (size.w * 0.5125, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            _1280x720 = Button('rect', (size.w * 0.7, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            
            Video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
            Audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
            Language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
            User_Center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
            Return_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')

            Full_Screen_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Video', 'Full_Screen' ), True, '#424769')
            _1366x768_text = Font(int(25 * size.w / 1280)).render('1366 x 768', True, '#424769')
            _1280x720_text = Font(int(25 * size.w / 1280)).render('1280 x 720', True, '#424769')
            

        #After all the object has been updated, change the variable to False
        change_size = False

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [Video, Audio, Language, User_Center, Return]:
            item.Blit(0,0)
        
        for item in [Full_Screen, _1366x768, _1280x720]:
            item.Blit(0,10)

        #Change colors if the mouse hover above
        for button in [Audio, Language, User_Center, Return]:
            button.Change_Color(mouse_pos, 0 , 0)

        for button in [Full_Screen, _1366x768, _1280x720]:
            button.Change_Color(mouse_pos, 0 , 10)


        #Blit Settings Text onto screen
        screen.blit(Video_text, Video_text.get_rect(center = (Video.rect.center)))
        screen.blit(Audio_text, Audio_text.get_rect(center = (Audio.rect.center)))
        screen.blit(Language_text, Language_text.get_rect(center = (Language.rect.center)))
        screen.blit(User_Center_text, User_Center_text.get_rect(center = (User_Center.rect.center)))
        screen.blit(Return_text, Return_text.get_rect(center = (Return.rect.center)))

        #Blit Video Texts onto screen
        screen.blit(Full_Screen_text, Full_Screen_text.get_rect(center = (Full_Screen.rect.center)))
        screen.blit(_1366x768_text, _1366x768_text.get_rect(center = (_1366x768.rect.center)))
        screen.blit(_1280x720_text, _1280x720_text.get_rect(center = (_1280x720.rect.center)))

        #Mouse Animation
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Audio_Menu(prev_menu, set_char, race_length):
    global music_volume, sfx_volume
    
    #Load Assets
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))

    Video = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Audio = Draw_to_Screen('rect', Video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    music_slider = pg.rect.Rect((0, 0), (300 * size.w/1280, 20 * size.h/720))
    music_slider.center = (size.w * 0.7, size.h * 0.25)

    music_circle = pg.rect.Rect((0,0), (30 * size.w/1280, 30 * size.w/1280))
    music_circle.center = (music_volume * (music_slider.right - music_slider.left) + music_slider.left, size.h * 0.25)

    sfx_slider = pg.rect.Rect((0, 0), (300 * size.w/1280, 20 * size.h/720))
    sfx_slider.center = (size.w * 0.7, size.h * 0.4)

    sfx_circle = pg.rect.Rect((0,0), (30 * size.w/1280, 30 * size.w/1280))
    sfx_circle.center = (sfx_volume * (sfx_slider.right - sfx_slider.left) + sfx_slider.left, size.h * 0.4)

    Video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
    Audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
    Language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
    User_Center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
    Return_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')

    music_text = Font(int(25*size.w/1280)).render(Updt_Lang(lang, 'Audio', 'Music' ), True, '#FFFFFF')
    sfx_text = Font(int(25*size.w/1280)).render(Updt_Lang(lang, 'Audio', 'SFX' ), True, '#FFFFFF')

    while True:

        #Position of the mouse
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to different setting menus
                if Video.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Menu(prev_menu, set_char, race_length)

                if Language.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Menu(prev_menu, set_char, race_length)

                if User_Center.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Menu(prev_menu, set_char, race_length)

                #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Start Menu':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_length)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_length)


        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Draw the music sliders
        pg.draw.rect(screen, 'light grey', music_slider, 0, 15)
        pg.draw.rect(screen, '#000000', music_circle, 0, 30)
        pg.draw.rect(screen, 'light grey', sfx_slider, 0, 15)
        pg.draw.rect(screen, '#000000', sfx_circle, 0, 30)


        #Change the music settings when mouse is pressed onto the circle
        keys = pg.mouse.get_pressed()

        if (music_circle.collidepoint(mouse_pos) and keys[0] == True):
            
            #Move music circle with mouse
            music_circle.center = (mouse_pos[0], size.h * 0.25)
            if music_circle.left <= music_slider.left: music_circle.left = music_slider.left
            if music_circle.right >= music_slider.right: music_circle.right = music_slider.right

            #Change music
            music_volume = round((music_circle.center[0] - music_slider.midleft[0]) / (300 * size.w/1280), 2)
            if music_volume <= 0.05: music_volume = 0
            if music_volume >= 0.95: music_volume = 1.0

            music_channels.set_volume(music_volume)

        elif (sfx_circle.collidepoint(mouse_pos) and keys[0] == True):

            #Move sfx circle with mouse
            sfx_circle.center = (mouse_pos[0], size.h * 0.4)
            if sfx_circle.left <= sfx_slider.left: sfx_circle.left = sfx_slider.left
            if sfx_circle.right >= sfx_slider.right: sfx_circle.right = sfx_slider.right

            #Change music
            sfx_volume = round((sfx_circle.center[0] - sfx_slider.midleft[0]) / (300 * size.w/1280), 2)
            if sfx_volume <= 0.05: sfx_volume = 0
            if sfx_volume >= 0.95: sfx_volume = 1.0

            sfx_channels.set_volume(sfx_volume)

        #Blit Assets onto screen
        for item in [Video, Audio, Language, User_Center, Return]:
            item.Blit(0,0)

        #Change colors if the mouse hover above
        for button in [Video, Language, User_Center, Return]:
            button.Change_Color(mouse_pos, 0 ,0)
        
        #Blit Settings Text onto screen
        screen.blit(Video_text, Video_text.get_rect(center = (Video.rect.center)))
        screen.blit(Audio_text, Audio_text.get_rect(center = (Audio.rect.center)))
        screen.blit(Language_text, Language_text.get_rect(center = (Language.rect.center)))
        screen.blit(User_Center_text, User_Center_text.get_rect(center = (User_Center.rect.center)))
        screen.blit(Return_text, Return_text.get_rect(center = (Return.rect.center)))

        screen.blit(music_text, music_text.get_rect(midleft = (size.w * 0.35, size.h * 0.25)))
        screen.blit(sfx_text, sfx_text.get_rect(midleft = (size.w * 0.35, size.h * 0.4)))

        #Mouse animation
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Language_Menu(prev_menu, set_char, race_length):
    global lang
    Change_Language = True

    #Load Assets
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))

    Video = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Audio = Button('rect', Video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d','#5d648c', None, None)
    Language = Draw_to_Screen('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    User_Center = Button('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    Choose_US = Button('rect', (size.w*0.375, size.h * 0.2), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    Choose_VN = Button('rect', (size.w*0.625, size.h * 0.2), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)

    Choose_US_text = Font(int(25 * size.w / 1280)).render('English', True, '#424769')
    Choose_VN_text = Font(int(25 * size.w / 1280)).render('Tiếng Việt', True, '#424769')

    while True:

        #Position of the mouse
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Change global langauge settings
                if Choose_US.Mouse_Click(mouse_pos) == True:
                    sfx_channels.play(interface)
                    Change_Language = True
                    lang = 'US'

                if Choose_VN.Mouse_Click(mouse_pos) == True:
                    sfx_channels.play(interface)
                    Change_Language = True
                    lang = 'VN'

                #Go to different setting menus
                if Video.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Menu(prev_menu, set_char, race_length)

                if Audio.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Menu(prev_menu, set_char, race_length)

                if User_Center.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Menu(prev_menu, set_char, race_length)

                #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Start Menu':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_length)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_length)

        #Update global lang
        if Change_Language == True:
            Video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
            Audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
            Language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
            User_Center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
            Return_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')

        #After update, return variable to False
        Change_Language == False

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [Choose_US, Choose_VN]:
            item.Blit(0,10)
        
        for item in [Video, Audio, Language, User_Center, Return]:
            item.Blit(0,0)

        #Change colors if the mouse hover above
        for button in [Choose_US, Choose_VN]:
            button.Change_Color(mouse_pos, 0 ,10)

        for button in [Video, Audio, User_Center, Return]:
            button.Change_Color(mouse_pos, 0 ,0)
        
        #Blit settings text onto the screen
        screen.blit(Video_text, Video_text.get_rect(center = (Video.rect.center)))
        screen.blit(Audio_text, Audio_text.get_rect(center = (Audio.rect.center)))
        screen.blit(Language_text, Language_text.get_rect(center = (Language.rect.center)))
        screen.blit(User_Center_text, User_Center_text.get_rect(center = (User_Center.rect.center)))
        screen.blit(Return_text, Return_text.get_rect(center = (Return.rect.center)))

        screen.blit(Choose_US_text, Choose_US_text.get_rect(center = (Choose_US.rect.center)))
        screen.blit(Choose_VN_text, Choose_VN_text.get_rect(center = (Choose_VN.rect.center)))

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def User_Center_Menu(prev_menu, set_char, race_length):

    #Load Assets
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))

    Video = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Audio = Button('rect', Video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    User_Center = Draw_to_Screen('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    

    Video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
    Audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
    Language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
    User_Center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
    Return_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')

    while True:

        #Get mouse position
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to different setting menus
                if Video.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Menu(prev_menu, set_char, race_length)

                if Audio.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Menu(prev_menu, set_char, race_length)

                if Language.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Menu(prev_menu, set_char, race_length)

                #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Start Menu':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_length)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_length)

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [Video, Audio, Language, User_Center, Return]:
            item.Blit(0,0)


        #Change colors if the mouse hover above
        for button in [Video, Audio, Language, Return]:
            button.Change_Color(mouse_pos, 0 ,0)
        
        #Blit text onto the screen
        screen.blit(Video_text, Video_text.get_rect(center = (Video.rect.center)))
        screen.blit(Audio_text, Audio_text.get_rect(center = (Audio.rect.center)))
        screen.blit(Language_text, Language_text.get_rect(center = (Language.rect.center)))
        screen.blit(User_Center_text, User_Center_text.get_rect(center = (User_Center.rect.center)))
        screen.blit(Return_text, Return_text.get_rect(center = (Return.rect.center)))

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

#Logo Animation
def Start_Animation():

    #set the alpha value for the screen
    alpha = 250

    #Get logo
    logo = pg.transform.scale(pg.image.load('Assets/icon/Settings/HCMUS_logo.png'), (size.w / 3, size.w / 3))
    logo_rect = logo.get_rect(center = (size.w/2, size.h/2))

    while True:
        alpha += 1.5
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            #Play mouse animation
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))
            
        screen.fill(0)

        if alpha < 180 and alpha > 0:
            #show the logo then fade it out shortly afterwards
            logo.set_alpha(int(255 * sin(rad(alpha))))
            screen.blit(logo, logo_rect)

        elif alpha > 250:
            #if alpha then reaches 250, move onto login screen
            Login('', '')

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

#Login
def Login(username, password):
    alpha = 0

    #just stuff for FPS ignore it
    fps = 0
    tru_fps = 0

    #To know which box the user click (username or password)
    insert = ''

    #Load Assets
    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))

    signup_select = Button('text', None, None, None, None, Updt_Lang(lang, 'Login', 'Select_Signup'), Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.35, size.h * 0.178))
    forgot_password = Button('text', None, None, None, None, Updt_Lang(lang, 'Login', 'Forgot_Password'), Font(int(15 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.405, size.h * 0.64))

    username_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    login_button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)
    faceID_button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)

    Quit = Button('image', None, None, 'Assets/icon/Settings/shutdown_01.png', (60*size.w/1280, 60* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shutdown_02.png', (size.w * 0.03, size.h * 0.95))

    welcome = Font(int(60 * size.w / 1280)).render (Updt_Lang(lang, 'Login', 'Title'), True, '#ffffff')
    login_select = Font(int(20 * size.w / 1280)).render(Updt_Lang(lang,'Login', 'Select_Login'), True, '#d69869')
    username_box_text = Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Username_text'), True, '#424769')
    password_box_text = Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Password_text'), True, '#424769')
    login_button_text = Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Login_Button'), True, '#424769')
    faceID_button_text = Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'FaceID_Button'), True, '#424769')

    login_failed = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Login_Failed'), True, "#FF0000")


    while True:
        alpha -= 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.KEYDOWN:
                
                #User clicked username
                if insert == 'username':
                    if event.key == pg.K_BACKSPACE:

                        username = username[:-1]
                    else:
                        username += event.unicode

                #User clicked password
                elif insert == 'password':
                    if event.key == pg.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

            if event.type == pg.MOUSEBUTTONDOWN:
                #Play mouse animation
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                if Quit.Mouse_Click(mouse_pos):
                    Shutdown()
                
                #Go to Sign up Page
                if (signup_select.Mouse_Click(mouse_pos)):
                    Signup('', '')

                #To know if user click on username, password box or not
                if username_box.Mouse_Click(mouse_pos):
                    insert = 'username'
                elif password_box.Mouse_Click(mouse_pos):
                    insert = 'password'
                else:
                    insert = ''

                #When user submit Login, check for validity and go to Title Screen if good
                if (login_button.Mouse_Click(mouse_pos)):
                    current_user = User_Data(username, password)
                    if current_user.Login():
                        Title(True)
                    else:
                        alpha = 500

            #Debug: FPS
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        #Language Logics: Not how you would do it but im tired ok?


        screen.fill('#2d3250')
        screen.blit(bg, (size.w*0.125, size.h*0.125))
        pg.draw.rect(screen, '#424769', [size.w*0.125, size.h*0.125, size.w*0.375, size.h * 0.75])

        #Draw the what the user typed in
        username_input = Font(int(13 * size.w / 1280)).render(username, True, '#FFFFFF')
        password_input = Font(int(13 * size.w / 1280)).render((len(password) - 1) * '*', True, '#FFFFFF')

        #Blit Assets onto the screen
        for item in [signup_select, username_box, password_box, forgot_password, login_button, faceID_button, Quit]:
            item.Blit(0,10)

        #Change colors if the mouse hover above
        for button in [signup_select, username_box, password_box, login_button, faceID_button, forgot_password, Quit]:
            button.Change_Color(mouse_pos, 0 ,10)
        
        #Blit Texts onto the screen
        screen.blit(login_select      ,   login_select.get_rect(center = (size.w * 0.265, size.h * 0.178)))
        screen.blit(welcome           ,   welcome.get_rect(center = (size.w * 0.3125, size.h * 0.3)))
        screen.blit(username_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.41)))
        screen.blit(password_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.54)))
        screen.blit(login_button_text ,   login_button_text.get_rect(center = (login_button.rect.center)))
        screen.blit(faceID_button_text,   faceID_button_text.get_rect(center = (faceID_button.rect.center)))
        screen.blit(username_input, username_input.get_rect(midleft = (size.w * 0.19, size.h * 0.45)))
        screen.blit(password_input, password_input.get_rect(midleft = (size.w * 0.19, size.h * 0.58)))
        
        #If error then set alpha so message appears then slowly fade away
        login_failed.set_alpha(alpha)
        screen.blit(login_failed, login_failed.get_rect(center = (size.w/2, size.h/2)))

        mouse_animation.update()
        mouse_animation.draw(screen)
        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
        
        pg.time.Clock().tick(60)
        pg.display.update()

#Sign up
def Signup(username, password):
    global lang

    #just stuff for FPS ignore it
    fps = 0
    tru_fps = 0

    #Login Logics

    repeat_password = password

    #To know which box the user click (username or password)
    insert = ''

    password_mismatch_alpha = 0
    password_length_error_alpha = 0
    username_alpha = 0
    existed_alpha = 0

    #Load Assets
    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))
    
    username_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    repeat_password_box = Button('rect', (size.w * 0.175, size.h * 0.645), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    
    signup_button = Button('rect', (size.w * 0.175, size.h * 0.775), (size.w*0.275, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)

    login_select = Button('text', None, None, None, None, Updt_Lang(lang, 'Sign_Up', 'Select_Login'), Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.265, size.h * 0.178))

    Quit = Button('image', None, None, 'Assets/icon/Settings/shutdown_01.png', (60*size.w/1280, 60* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shutdown_02.png', (size.w * 0.03, size.h * 0.95))
    
    username_error = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Username_Error'), True, "#FF0000")
    password_mismatch = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Password_Mismatch'), True, "#FF0000")
    password_length_error = Font(int(50 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Password_Length_Error'), True, "#FF0000")
    existed_error = Font(int(50 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Existed'), True, "#FF0000")

    welcome = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Title'), True, '#ffffff')
    signup_select = Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Select_Signup'), True, '#d69869')
    username_box_text = Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Username_text'), True, '#424769')
    password_box_text = Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Password_text'), True, '#424769')
    signup_button_text = Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Signup_button'), True, '#424769')


    while True:
        username_alpha -= 7.5
        password_mismatch_alpha -= 7.5
        password_length_error_alpha -= 7.5
        existed_alpha -= 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            #Play mouse animation
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                if Quit.Mouse_Click(mouse_pos):
                    Shutdown()

                #Go to Login Page
                if(login_select.Mouse_Click(mouse_pos)):
                    Login('', '')

                #To know which box user clicked
                if username_box.Mouse_Click(mouse_pos):
                    insert = 'username'

                elif password_box.Mouse_Click(mouse_pos):
                    insert = 'password'

                elif repeat_password_box.Mouse_Click(mouse_pos):
                    insert = 'repeat_password'

                else:
                    insert = ''

                #When user submit Sign up, check for validity and go to Title Screen if good
                if signup_button.Mouse_Click(mouse_pos):
                    current_user = User_Data(username, password)
                    if len(password) < 8:
                        password_length_error_alpha = 500

                    elif password != repeat_password:
                        password_mismatch_alpha = 500

                    elif (current_user.Sign_Up_Validate() == False):
                        existed_alpha = 500

                    else :
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Enter_Code(username, password, hashlib.sha256('1000'.encode()).hexdigest())

                #User clicked username
            if event.type == pg.KEYDOWN:

                if insert == 'username':
                    if event.key == pg.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                        
                #User clicked password
                elif insert == 'password':
                    if event.key == pg.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

                #User clicked re-enter password
                elif insert == 'repeat_password':
                    if event.key == pg.K_BACKSPACE:
                        repeat_password = repeat_password[:-1]
                    else:
                        repeat_password += event.unicode

                               
            #Debug: FPS
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0
        
        screen.fill('#2d3250')
        screen.blit(bg, (size.w*0.125, size.h*0.125))
        pg.draw.rect(screen, '#424769', [size.w*0.125, size.h*0.125, size.w*0.375, size.h * 0.75])

        #Draw the what the user typed in
        username_input = Font(int(12 * size.w / 1280)).render(username, True, '#FFFFFF')
        password_input = Font(int(12 * size.w / 1280)).render(len(password) * '*', True, '#FFFFFF')
        repeat_password_input = Font(int(12 * size.w / 1280)).render(len(repeat_password) * '*', True, '#FFFFFF')

        #Blit Assets onto screen
        for item in [login_select, username_box, password_box, repeat_password_box, signup_button, Quit]:
            item.Blit(0,10)

        #Change colors if the mouse hover above
        for button in [login_select, username_box, password_box, signup_button, repeat_password_box, Quit]:
            button.Change_Color(mouse_pos, 0 ,10)

        #Blit Texts onto the screen
        screen.blit(signup_select     ,   signup_select.get_rect(center = (size.w * 0.35, size.h * 0.178)))
        screen.blit(welcome           ,   welcome.get_rect(center = (size.w * 0.3125, size.h * 0.3)))
        screen.blit(username_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.41)))
        screen.blit(password_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.54)))
        screen.blit(Font(int(13 * size.w/1280)).render(Updt_Lang(lang, 'Sign_Up', 'Repeat_Password_text'), True, "#424769"),
                     username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.67)))
        screen.blit(signup_button_text ,   signup_button_text.get_rect(center = (signup_button.rect.center)))
        screen.blit(username_input, username_input.get_rect(midleft = (size.w * 0.19, size.h * 0.45)))
        screen.blit(password_input, password_input.get_rect(midleft = (size.w * 0.19, size.h * 0.58)))
        screen.blit(repeat_password_input, repeat_password_input.get_rect(midleft = (size.w * 0.19, size.h * 0.71)))


        #If error then set alpha so message appears then slowly fade away

        username_error.set_alpha(username_alpha)
        screen.blit(username_error,  username_error.get_rect(center = (size.w/2, size.h/2)))

        password_mismatch.set_alpha(password_mismatch_alpha)
        screen.blit(password_mismatch,  password_mismatch.get_rect(center = (size.w/2, size.h/2)))

        password_length_error.set_alpha(password_length_error_alpha)
        screen.blit(password_length_error,  password_length_error.get_rect(center = (size.w/2, size.h/2)))

        existed_error.set_alpha(existed_alpha)
        screen.blit(existed_error,  existed_error.get_rect(center = (size.w/2, size.h/2)))

        mouse_animation.update()
        mouse_animation.draw(screen)
        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
        
        pg.time.Clock().tick(60)
        pg.display.update()

#Enter confirmation code
def Enter_Code(username, password, en_code):
    insert = False
    verify_code = ''
    wrong_code_alpha = 0

    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg.convert(), (size.w, size.h))

    box = pg.rect.Rect((0,0) , (size.w * 0.5, size.h * 0.5))
    box.center = (size.w * 0.5, size.h * 0.5)

    box_outline = pg.rect.Rect((0,0) , (size.w * 0.5005, size.h * 0.5005))
    box_outline.center = (size.w * 0.5, size.h * 0.5)

    title = Font(int(40*size.w/1280)).render("Verify Your Emails", True, "#FFFFFF")

    prompt = Font(int(20*size.w/1280)).render("Check your email inbox for verification code", True, '#FFFFFF')
    
    verify = Button('rect', (size.w * 0.3125, size.h * 0.425), (size.w*0.4, size.h * 0.125), None, None, None, None, '#676f9d', '#5d648c', None, None)
    verify.rect.center = (size.w * 0.5, size.h * 0.525)

    verify_text = Font(int(15*size.w/1280)).render("Enter your verification code", True, '#424769')

    submit = Button('rect', (size.w * 0.175, size.h * 0.425), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None, None)
    submit.rect.center = (size.w * 0.5, size.h * 0.675)

    submit_text = Font(int(20*size.w/1280)).render("Submit", True, '#424769')

    close = Button('image', None, None, 'Assets/Obstacles/frame_box.png', (48*size.w/1280, 48*size.w/1280), None, None, None, None , 'Assets/Obstacles/frame_box.png', (0,0))
    close.rect.center = box_outline.topright

    wrong_code = Font(int(60*size.w/1280)).render("Incorrect Verification Code", True, '#FF0000')

     
    while True:
        wrong_code_alpha -= 7.5
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to Login Page
                if(verify.Mouse_Click(mouse_pos)):
                    insert = True
                else:
                    insert = False
                
                if (close.Mouse_Click(mouse_pos)):
                    Signup(username, password)
                
                if (submit.Mouse_Click(mouse_pos)):
                    if hashlib.sha256(verify_code.encode()).hexdigest() == en_code:
                        current_user = User_Data(username, password)

                        if current_user.Sign_Up():
                            Title(True)

                    else:
                        wrong_code_alpha = 500

            if event.type == pg.KEYDOWN:
                if insert:
                    if event.key == pg.K_BACKSPACE:
                        verify_code = verify_code[:-1]
                    else:
                        verify_code += event.unicode
        
        screen.blit(bg, (0,0))
        enter_verify_text = Font(int(50*size.w/1280)).render(verify_code, True, '#FFFFFF')

        pg.draw.rect(screen, '#424769', box, 0, 10)
        pg.draw.rect(screen, '#000000', box_outline, 5, 10)

        verify.Blit(0,10)
        submit.Blit(0,10)
        close.Blit(0,10)

        verify.Change_Color(mouse_pos, 0 ,10)
        submit.Change_Color(mouse_pos, 0 ,10)

        screen.blit(enter_verify_text, enter_verify_text.get_rect(center = (verify.rect.center)))
        screen.blit(title, title.get_rect(center = (size.w/2, size.h * 0.325)))
        screen.blit(prompt, prompt.get_rect(center = (size.w/2, size.h * 0.385)))
        screen.blit(submit_text, submit_text.get_rect(center = (submit.rect.center)))

        wrong_code.set_alpha(wrong_code_alpha)
        screen.blit(wrong_code, wrong_code.get_rect(center = (submit.rect.center)))

        if (insert == False and verify_code == ''):
            screen.blit(verify_text, verify_text.get_rect(center = (verify.rect.center)))

        pg.time.Clock().tick(60)
        pg.display.update()

#Title Screen
def Title(restart_music):
    fps = 0
    tru_fps = 0
    alpha = 0

    #If enter_game becomes True then stop button functions
    enter_game = False

    #Restart the music
    if restart_music:
        music_channels.play(title_music, loops = -1)

    #Load Assets
    Background = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert_alpha(), (size.w*1.075, size.h*1.075))
        
    Quit = Button('image', None, None, 'Assets/icon/Settings/shutdown_01.png', (60*size.w/1280, 60* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shutdown_02.png', (size.w * 0.03, size.h * 0.95))

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.97, size.h * 0.05))
    
    #Language Logics
    Prompt = Font(int(25 * size.w/1280)).render(Updt_Lang(lang, 'Title', 'Prompt'), True, '#000000')

    while True:
        alpha += 5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #If Quit button is pressed, exit the game only when enter_game is False
                if Quit.Mouse_Click(mouse_pos) == True and enter_game == False:
                    Shutdown()
                
                #Go to Settings Page
                if (Settings.Mouse_Click(mouse_pos) == True and enter_game == False):
                    sfx_channels.play(button_click)
                    pg.image.save(screen, 'Assets/temps/temp.png')
                    Video_Menu('Start Menu', '', '')
                
                #If user click anywhere on the screen, set alpha to 255 and enter_game = True to stop all button function
                elif enter_game == False:
                    enter_game = True
                    alpha = 255

            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0
        
        #Background moves with cursor
        Bg = Background_Animation(Background, (size.w / 2, size.h / 2), mouse_pos)

        Title = Font(int(100 * size.w / 1280)).render('Racing Bet', True, "#000000")
        
        screen.fill(0)

        #Set alpha for fade in animation
        for stuff in [Settings.image, Quit.image, Background]:
            stuff.set_alpha(alpha)

        #Make the prompt continuously flashing
        Prompt.set_alpha(255 * abs(sin(rad(alpha))))
        Bg.Draw()

        #Blit Assets onto screen
        for item in  [Quit, Settings]:
            item.Blit(0,10)

        screen.blit(Title, Title.get_rect(center = (size.w * 0.5, size.h *0.25 )))
        screen.blit(Prompt, Prompt.get_rect(center = (size.w * 0.5, size.h * 0.75)))

        #Fade out animaion
        if enter_game:
            alpha -= 15
            if alpha < -20:
                In_Game_Menu(-20)
        
        #Change colors if the mouse hover above
        else:
            for button in [Quit, Settings]:
                button.Change_Color(mouse_pos, 0 ,10)
        
        mouse_animation.update()
        mouse_animation.draw(screen)

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))

        pg.time.Clock().tick(60)
        pg.display.update()

#In Game Screen
def In_Game_Menu(alpha):
    #Mainly for the sake of animation. Target menu is the menu that player selected
    Change_Menu = False
    Target_Menu = ''
    fps = 0
    tru_fps = 0

    #Load Assets
    Background = pg.transform.smoothscale(pg.image.load('Assets/background/Street/citystreet.png').convert_alpha(), (512, 288))
    Background = pg.transform.smoothscale(Background, (size.w*1.075, size.h*1.075))

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.97, size.h * 0.05))
    
    Return = Button('image', None, None, 'Assets/icon/Settings/return_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/return_02.png', (size.w * 0.03, size.h * 0.95))

    Coins_box = pg.rect.Rect((0,0), ((size.w*0.25, size.h * 0.05)))
    Coins_box.center = ((size.w*0.775, size.h * 0.275))

    Coins = pg.image.load('Assets/coin.png').convert_alpha()
    Coins = pg.transform.rotozoom(Coins, 0, 1.5)


    Play = Button('image', None, None, 'Assets/icon/Settings/play.png', (size.w*0.25, size.h * 0.15), None, None, None, None, 'Assets/icon/Settings/play_hover.png', (size.w*0.775, size.h * 0.4))
    Mini_Game = Button('image', None, None, 'Assets/icon/Settings/minigame.png', (size.w*0.25, size.h * 0.15), None, None, None, None, 'Assets/icon/Settings/minigame_hover.png', (size.w*0.775, size.h * 0.6))
    Rank = Button('image', None, None, 'Assets/icon/Settings/rank.png', (size.w*0.25, size.h * 0.15), None, None, None, None, 'Assets/icon/Settings/rank_hover.png', (size.w*0.775, size.h * 0.8))
    
    
    while True:
        alpha += 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Set the alpha for fade out animation when user click on a menu
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

                    #Go to Settings Page
                    if Settings.Mouse_Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Menu('In_Game_Menu', '', '')
                    
                    #Return to title screen
                    if Return.Mouse_Click(mouse_pos):
                        Title(True)
            
            #Debug: FPS
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        screen.fill(0)

        #Background move with cursor
        Bg = Background_Animation(Background, (size.w / 2, size.h / 2), mouse_pos)

        #Fade in animations
        for item in [Background, Settings.image, Play.image, Mini_Game.image, Rank.image, Return.image]:
            item.set_alpha(alpha)

        Bg.Draw()

        #Load Assets onto screen
        for item in [Play, Mini_Game, Rank, Settings, Return]:
            item.Blit(0,10)

        pg.draw.rect(screen, "#FFFFFF", Coins_box, 2, 10)
        screen.blit(Coins, Coins.get_rect(center = (size.w*0.75, size.h * 0.275)))
        #Fade out animation logics
        if Change_Menu:
            alpha -= 15
            if Target_Menu == 'Play':
                if alpha < 0:
                    Choose_Character_Set(-20, '', '')
            elif Target_Menu == 'Mini Game':
                if alpha < 0:
                    Mini_Game_Menu()
            elif Target_Menu == 'Rank':
                if alpha < 0:
                    pass

        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        elif alpha > 225 and Change_Menu == False:
            for button in [Settings, Play, Mini_Game, Rank, Return]:
                button.Change_Color(mouse_pos, 0 ,10)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

def Mini_Game_Menu():
    global highest_scores, gold
    screen_size_display = (size.w, size.h) = (size.w, size.h)
    FPS = 60
    gravity = 0.6
    font = pg.font.Font('freesansbold.ttf', 20)

    black_color = (0,0,0)
    white_color = (255,255,255)
    bg_color = (235, 235, 235) 

    highest_scores = 0

    screen_layout_display = pg.display.set_mode(screen_size_display)
    coin_symbol = pg.image.load('Dino-Game/resources/coin.png').convert_alpha()
    coin_symbol = pg.transform.rotozoom(coin_symbol, 0 , 2)

    time_clock = pg.time.Clock()
    pg.display.set_caption("Dino Run ")

    jump_sound = pg.mixer.Sound('Dino-Game/sound/jump.wav')
    die_sound = pg.mixer.Sound('Dino-Game/sound/die.wav')
    checkPoint_sound = pg.mixer.Sound('Dino-Game/sound/checkPoint.wav')

    def load_image(
        name,
        sx=-1,
        sy=-1,
        colorkey=None,
        ):

        fullname = os.path.join('Dino-Game/resources', name)
        img = pg.image.load(fullname).convert()
        img = img.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey, pg.RLEACCEL)

        if sx != -1 or sy != -1:
            img = pg.transform.scale(img, (sx, sy))

        return (img, img.get_rect())

    def load_sprite_sheet(
            s_name,
            namex,
            namey,
            scx = -1,
            scy = -1,
            c_key = None,
            ):
        fullname = os.path.join('Dino-Game/resources', s_name)
        sh = pg.image.load(fullname).convert()
        sh = sh.convert()

        sh_rect = sh.get_rect()

        sprites = []

        sx = sh_rect.width/ namex
        sy = sh_rect.height/ namey

        for i in range(0, namey):
            for j in range(0, namex):
                rect = pg.Rect((j*sx,i*sy,sx,sy))
                img = pg.Surface(rect.size)
                img = img.convert()
                img.blit(sh,(0,0),rect)

                if c_key is not None:
                    if c_key == -1:
                        c_key = img.get_at((0, 0))
                    img.set_colorkey(c_key, pg.RLEACCEL)

                if scx != -1 or scy != -1:
                    img = pg.transform.scale(img, (scx, scy))

                sprites.append(img)

        sprite_rect = sprites[0].get_rect()

        return sprites,sprite_rect

    def gameover_display_message(rbtn_image, gmo_image):
        rbtn_rect = rbtn_image.get_rect()
        rbtn_rect.centerx = size.w / 2
        rbtn_rect.top = size.h * 0.52

        gmo_rect = gmo_image.get_rect()
        gmo_rect.centerx = size.w / 2
        gmo_rect.centery = size.h * 0.35

        screen_layout_display.blit(gmo_image, gmo_rect)

    def extractDigits(num):
        if num > -1:
            d = []
            i = 0
            while(num / 10 != 0):
                d.append(num % 10)
                num = int(num / 10)

            d.append(num % 10)
            for i in range(len(d),5):
                d.append(0)
            d.reverse()
            return d

    class Dino():
        def __init__(self, sx=-1, sy=-1):
            self.imgs, self.rect = load_sprite_sheet('dino.png', 5, 1, sx, sy, -1)
            self.imgs1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sy, -1)
            self.rect.bottom = int(0.98 * size.h)
            self.rect.left = size.w / 15
            self.image = self.imgs[0]
            self.index = 0
            self.counter = 0
            self.score = 0
            self.pre_score = 0
            self.jumping = False
            self.dead = False
            self.ducking = False
            self.blinking = False
            self.movement = [0,0]
            self.jumpSpeed = 11.5

            self.stand_position_width = self.rect.width
            self.duck_position_width = self.rect1.width

        def draw(self):
            screen_layout_display.blit(self.image, self.rect)

        def checkbounds(self):
            if self.rect.bottom > int(0.98 * size.h):
                self.rect.bottom = int(0.98 * size.h)
                self.jumping = False

        def update(self):
            if self.jumping:
                self.movement[1] = self.movement[1] + gravity

            if self.jumping:
                self.index = 0
            elif self.blinking:
                if self.index == 0:
                    if self.counter % 400 == 399:
                        self.index = (self.index + 1)%2
                else:
                    if self.counter % 20 == 19:
                        self.index = (self.index + 1)%2

            elif self.ducking:
                if self.counter % 5 == 0:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 5 == 0:
                    self.index = (self.index + 1)%2 + 2

            if self.dead:
                self.index = 4

            if not self.ducking:
                self.image = self.imgs[self.index]
                self.rect.width = self.stand_position_width
            else:
                self.image = self.imgs1[(self.index) % 2]
                self.rect.width = self.duck_position_width

            self.rect = self.rect.move(self.movement)
            self.checkbounds()

            if not self.dead and self.counter % 7 == 6 and self.blinking == False:
                self.pre_score += 1
                if self.pre_score % 5 == 0:
                    self.score += 1

                if self.pre_score % 100 == 0 and self.pre_score != 0:
                    if pg.mixer.get_init() != None:
                        checkPoint_sound.play()

            self.counter = (self.counter + 1)

    class Cactus(pg.sprite.Sprite):
        def __init__(self, speed=5, sx=-1, sy=-1):
            pg.sprite.Sprite.__init__(self,self.containers)
            self.imgs, self.rect = load_sprite_sheet('cactus-small.png', 3, 1, sx, sy, -1)
            self.rect.bottom = int(0.98 * size.h)
            self.rect.left = size.w + self.rect.width
            self.image = self.imgs[randrange(0, 3)]
            self.movement = [-1*speed,0]

        def draw(self):
            screen_layout_display.blit(self.image, self.rect)

        def update(self):
            self.rect = self.rect.move(self.movement)

            if self.rect.right < 0:
                self.kill()

    class birds(pg.sprite.Sprite):
        def __init__(self, speed=5, sx=-1, sy=-1):
            pg.sprite.Sprite.__init__(self,self.containers)
            self.imgs, self.rect = load_sprite_sheet('birds.png', 2, 1, sx, sy, -1)
            self.birds_height = [size.h * 0.95, size.h * 0.925, size.h * 0.875]
            self.rect.centery = self.birds_height[randrange(0, 3)]
            self.rect.left = size.w + self.rect.width
            self.image = self.imgs[0]
            self.movement = [-1*speed,0]
            self.index = 0
            self.counter = 0

        def draw(self):
            screen_layout_display.blit(self.image, self.rect)

        def update(self):
            if self.counter % 10 == 0:
                self.index = (self.index+1)%2
            self.image = self.imgs[self.index]
            self.rect = self.rect.move(self.movement)
            self.counter = (self.counter + 1)
            if self.rect.right < 0:
                self.kill()


    class Ground():
        def __init__(self,speed=-5):
            self.image,self.rect = load_image('ground.png',-1,-1,-1)
            self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
            self.rect.bottom = size.h
            self.rect1.bottom = size.h
            self.rect1.left = self.rect.right
            self.speed = speed

        def draw(self):
            screen_layout_display.blit(self.image, self.rect)
            screen_layout_display.blit(self.image1, self.rect1)

        def update(self):
            self.rect.left += self.speed
            self.rect1.left += self.speed

            if self.rect.right < 0:
                self.rect.left = self.rect1.right

            if self.rect1.right < 0:
                self.rect1.left = self.rect.right

    class Cloud(pg.sprite.Sprite):
        def __init__(self,x,y):
            pg.sprite.Sprite.__init__(self,self.containers)
            self.image,self.rect = load_image('cloud.png',int(90*30/42),30,-1)
            self.speed = 1
            self.rect.left = x
            self.rect.top = y
            self.movement = [-1*self.speed,0]

        def draw(self):
            screen_layout_display.blit(self.image, self.rect)

        def update(self):
            self.rect = self.rect.move(self.movement)
            if self.rect.right < 0:
                self.kill()

    class Scoreboard():
        def __init__(self,x=-1,y=-1):
            self.score = 0
            self.scre_img, self.screrect = load_sprite_sheet('numbers.png', 12, 1, 20, int(20 * 6 / 5), -1)
            self.image = pg.Surface((100,int(20*6/5)))
            self.rect = self.image.get_rect()
            if x == -1:
                self.rect.left = size.w * 0.85
            else:
                self.rect.left = x
            if y == -1:
                self.rect.top = size.h * 0.1
            else:
                self.rect.top = y

        def draw(self):
            screen_layout_display.blit(coin_symbol,(size.w*0.825, size.h * 0.1))
            screen_layout_display.blit(self.image, self.rect)
        
        def update(self,score):
            score_digits = extractDigits(score)
            self.image.fill(bg_color)
            for s in score_digits:
                self.image.blit(self.scre_img[s], self.screrect)
                self.screrect.left += self.screrect.width
            self.screrect.left = 0


    def introduction_screen():
        ado_dino = Dino(76 * size.w /1280, 80 * size.w / 1280)
        ado_dino.blinking = True
        starting_game = False

        t_ground,t_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
        t_ground_rect.left = size.w / 20
        t_ground_rect.bottom = size.h

        logo,l_rect = load_image('logo.png',size.w * 0.4,size.h * 0.2,-1)
        l_rect.centerx = size.w * 0.5
        l_rect.centery = size.h * 0.4
        while not starting_game:
            if pg.display.get_surface() == None:
                print("Couldn't load display surface")
                return True
            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return True
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE or event.key == pg.K_UP:
                            ado_dino.jumping = True
                            ado_dino.blinking = False
                            ado_dino.movement[1] = -1.05*ado_dino.jumpSpeed

            ado_dino.update()

            if pg.display.get_surface() != None:
                screen_layout_display.fill(bg_color)
                screen_layout_display.blit(t_ground[0], t_ground_rect)
                if ado_dino.blinking:
                    screen_layout_display.blit(logo, l_rect)
                ado_dino.draw()

                pg.display.update()

            time_clock.tick(FPS)
            if ado_dino.jumping == False and ado_dino.blinking == False:
                starting_game = True

    def gameplay():
        global highest_scores, gold
        gp = 8
        s_Menu = False
        g_Over = False
        g_exit = False
        gamer_Dino = Dino(76 * size.w /1280, 80 * size.w / 1280)
        new_grnd = Ground(-1*gp)
        score_boards = Scoreboard()
        highScore = Scoreboard(size.w * 0.78)
        counter = 0
        
        cactusan = pg.sprite.Group()
        smallBird = pg.sprite.Group()
        skyClouds = pg.sprite.Group()
        last_end_obs = pg.sprite.Group()

        Cactus.containers = cactusan
        birds.containers = smallBird
        Cloud.containers = skyClouds

        rbtn_image,rbtn_rect = load_image('replay_button.png',35,31,-1)
        gmo_image,gmo_rect = load_image('game_over.png',190,11,-1)
        
        t_images,t_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        ado_image = pg.Surface((22,int(11*6/5)))
        ado_rect = ado_image.get_rect()
        ado_image.fill(bg_color)
        ado_image.blit(t_images[10],t_rect)
        t_rect.left += t_rect.width
        ado_image.blit(t_images[11],t_rect)
        ado_rect.top = size.h * 0.1
        ado_rect.left = size.w * 0.73
        ado_image.blit(t_images[11],t_rect)
        
        while not g_exit:
            while s_Menu:
                pass
            while not g_Over:
                if pg.display.get_surface() == None:
                    print("Couldn't load display surface")
                    g_exit = True
                    g_Over = True
                else:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            g_exit = True
                            g_Over = True

                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_SPACE:
                                if gamer_Dino.rect.bottom == int(0.98 * size.h):
                                    gamer_Dino.jumping = True
                                    if pg.mixer.get_init() != None:
                                        jump_sound.play()
                                    gamer_Dino.movement[1] = -1.05 * gamer_Dino.jumpSpeed

                            if event.key == pg.K_DOWN:
                                if not (gamer_Dino.jumping and gamer_Dino.dead):
                                    gamer_Dino.ducking = True

                        if event.type == pg.KEYUP:
                            if event.key == pg.K_DOWN:
                                gamer_Dino.ducking = False
                for c in cactusan:
                    c.movement[0] = -1*gp
                    if pg.sprite.collide_mask(gamer_Dino,c):
                        gamer_Dino.dead = True
                        if pg.mixer.get_init() != None:
                            die_sound.play()

                for p in smallBird:
                    p.movement[0] = -1*gp
                    if pg.sprite.collide_mask(gamer_Dino,p):
                        gamer_Dino.dead = True
                        if pg.mixer.get_init() != None:
                            die_sound.play()

                if len(cactusan) < 2:
                    if len(cactusan) == 0:
                        last_end_obs.empty()
                        last_end_obs.add(Cactus(gp, 50 * size.w / 1280, 60 * size.w / 1280))
                    else:
                        for l in last_end_obs:
                            if l.rect.right < size.w*0.7 and randrange(0, 50) == 10:
                                last_end_obs.empty()
                                last_end_obs.add(Cactus(gp, 50 * size.w / 1280, 60 * size.w / 1280))

                if len(smallBird) == 0 and randrange(0,200) == 10 and counter > 500:
                    for l in last_end_obs:
                        if l.rect.right < size.w*0.8:
                            last_end_obs.empty()
                            last_end_obs.add(birds(gp, 46 * size.w / 1280, 40 * size.w / 1280))

                if len(skyClouds) < 5 and randrange(0,300) == 10:
                    Cloud(size.w, randrange(int(size.h / 5), int(size.h / 2)))

                gamer_Dino.update()
                cactusan.update()
                smallBird.update()
                skyClouds.update()
                new_grnd.update()
                score_boards.update(gamer_Dino.score)
                
                if pg.display.get_surface() != None:
                    screen_layout_display.fill(bg_color)
                    new_grnd.draw()
                    skyClouds.draw(screen_layout_display)
                    score_boards.draw()
                    if highest_scores != 0:
                        highScore.draw()
                        screen_layout_display.blit(ado_image, ado_rect)
                    cactusan.draw(screen_layout_display)
                    smallBird.draw(screen_layout_display)
                    gamer_Dino.draw()

                    pg.display.update()
                time_clock.tick(FPS)
                gold = gamer_Dino.score
                if gamer_Dino.dead:
                    print(gold)
                    g_Over = True


                if counter%700 == 699:
                    new_grnd.speed -= 1
                    gp += 1

                counter = (counter + 1)

            if g_exit:
                break

            while g_Over:
                if pg.display.get_surface() == None:
                    print("Couldn't load display surface")
                    g_exit = True
                    g_Over = False
                else:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            sys.exit()
                highScore.update(highest_scores)
                if pg.display.get_surface() != None:
                    gameover_display_message(rbtn_image, gmo_image)
                    if highest_scores != 0:
                        highScore.draw()
                        screen_layout_display.blit(ado_image, ado_rect)
                    pg.display.update()
                    
                SCREEN = pg.display.set_mode((size.w, size.h))
                while True:
                    SCREEN.fill((255, 255, 255))
                    text = font.render("GAME OVER", True, (0, 0, 0))
                    score = font.render("Your gold       : " + str(gold), True, (0, 0, 0))
                    scoreRect = score.get_rect()
                    scoreRect.center = (size.w // 2, size.h // 2 + 50)
                    SCREEN.blit(score, scoreRect)
                    textRect = text.get_rect()
                    textRect.center = (size.w // 2, size.h // 2)
                    SCREEN.blit(text, textRect)
                    SCREEN.blit(coin_symbol,(663 * size.w / 1280 , 396 * size.w /1280))
                    pg.display.update()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            sys.exit()
                        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            In_Game_Menu(-20)
                    time_clock.tick(FPS)
                
        pg.quit()
        quit()

    def main():
        isGameQuit = introduction_screen()
        if not isGameQuit:
            gameplay()

    main()
#Choose character
def Choose_Character_Set(alpha, character_set, race_length):
    Change_Menu = False
    fps = 0
    tru_fps = 0

    #Load Assets
    Background = pg.transform.scale(pg.image.load('Assets/icon/Settings/Cafe.png').convert_alpha(), (512, 288))
    Background = pg.transform.smoothscale(Background, (size.w*1.15, size.h*1.15))

    User_Info_Tab = pg.Surface((size.w, size.h * 0.1), pg.SRCALPHA)
    User_Info_Tab.fill('#2d3250')

    SetA = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.1, size.h * 0.25)) 
    SetB = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.3, size.h * 0.25))
    SetC = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.5, size.h * 0.25))
    SetD = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.7, size.h * 0.25))
    SetE = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.9, size.h * 0.25))

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.97, size.h * 0.05))
    
    Continue = Button('image', None, None, 'Assets/icon/Settings/continue_01.png', (60*size.w/1280, 60* size.w/1280), None, None, None, None, 'Assets/icon/Settings/continue_02.png', (size.w*0.975, size.h * 0.95))

    Return = Button('image', None, None, 'Assets/icon/Settings/return_01.png', (60*size.w/1280, 60* size.w/1280), None, None, None, None, 'Assets/icon/Settings/return_02.png', (size.w*0.025, size.h * 0.95)) 

    while True:
        alpha += 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to Settings Page
                if Change_Menu == False:
                    if Settings.Mouse_Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Menu('Choose_Character_Set', character_set, race_length)
                    
                    #Change character set when user click on it
                    if Continue.Mouse_Click(mouse_pos) and character_set != '':
                        Choose_Race_Length(-20, character_set, race_length)
                    if SetA.Mouse_Click(mouse_pos):
                        character_set = 'SetA'
                    if SetB.Mouse_Click(mouse_pos):
                        character_set = 'SetB'
                    if SetC.Mouse_Click(mouse_pos):
                        character_set = 'SetC'
                    if SetD.Mouse_Click(mouse_pos):
                        character_set = 'SetD'
                    if SetE.Mouse_Click(mouse_pos):
                        character_set = 'SetE'

                    #Return to In_Game_Menu with alpha of -20 for fade in animations
                    if Return.Mouse_Click(mouse_pos):
                        In_Game_Menu(-20)
            
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        screen.fill(0)

        #Background moves with cursor
        Bg = Background_Animation(Background, (size.w / 2, size.h / 2), mouse_pos)

        #Temporary: Show what you have selected
        Selected = Font(40).render(f'Selected: {character_set}', True, '#ffffff')

        #Fade in animations
        for stuff in [Background, User_Info_Tab, Return.image, Continue.image, Settings.image, SetA.image, SetB.image, SetC.image, SetD.image, SetE.image, Selected]:
            stuff.set_alpha(alpha)

        Bg.Draw()
        screen.blit(User_Info_Tab, (0,0))
        screen.blit(Selected, Selected.get_rect(center = (size.w/2, size.h/2)))

        #Blit assets onto screen
        for item in [Settings, Return, Continue, SetA, SetB, SetC, SetD, SetE]:
            item.Blit(0,10)

        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        if alpha > 225 and Change_Menu == False:
            for button in [Settings, Continue, Return, SetA, SetB, SetC, SetD, SetE]:
                button.Change_Color(mouse_pos, 0 ,10)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

#Choose race length
def Choose_Race_Length(alpha, character_set, race_length):
    Change_Menu = False
    fps = 0
    tru_fps = 0

    #Load Assets
    Background = pg.transform.scale(pg.image.load('Assets/icon/Settings/Cafe.png').convert_alpha(), (512, 288))
    Background = pg.transform.smoothscale(Background, (size.w*1.15, size.h*1.15))

    User_Info_Tab = pg.Surface((size.w, size.h * 0.1), pg.SRCALPHA)
    User_Info_Tab.fill('#2d3250')

    LengthA = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.25, size.h * 0.25)) 
    LengthB = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.5, size.h * 0.25))
    LengthC = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-2.png', (size.w * 0.75, size.h * 0.25))
    
    Settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.97, size.h * 0.05))
    
    Continue = Button('image', None, None, 'Assets/icon/Settings/continue_01.png', (60*size.w/1280, 60* size.w/1280), None, None, None, None, 'Assets/icon/Settings/continue_02.png', (size.w*0.975, size.h * 0.95))

    Return = Button('image', None, None, 'Assets/icon/Settings/return_01.png', (60*size.w/1280, 60* size.w/1280), None, None, None, None, 'Assets/icon/Settings/return_02.png', (size.w*0.025, size.h * 0.95)) 

    while True:
        alpha += 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))


                if Change_Menu == False:

                    #Go to Settings Page
                    if Settings.Mouse_Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Menu('Choose_Race_Length', character_set, race_length)

                    #Change character set when user click on it
                    if LengthA.Mouse_Click(mouse_pos):
                        race_length = 'Short'
                    if LengthB.Mouse_Click(mouse_pos):
                        race_length = 'Medium'
                    if LengthC.Mouse_Click(mouse_pos):
                        race_length = 'Long'
                    
                    #Debug: if user click start then print out what user has choosen 
                    if Continue.Mouse_Click(mouse_pos) and race_length != '':
                        print(f'Selected: {character_set}')
                        print(f'Selected: {race_length}')

                    #Return to Choose_Character screen and preserve what the user chose
                    if Return.Mouse_Click(mouse_pos):
                        Choose_Character_Set(-20, character_set, race_length)
            
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        screen.fill(0)

        #Background moves with cursor
        Bg = Background_Animation(Background, (size.w / 2, size.h / 2), mouse_pos)

        #Temporary:
        Selected = Font(40).render(f'Selected: {race_length}', True, '#ffffff')

        #Fade in animation
        for item in [Background, User_Info_Tab, Return.image, Continue.image, Settings.image, LengthA.image, LengthB.image, LengthC.image, Selected]:
            item.set_alpha(alpha)

        
        Bg.Draw()
        screen.blit(User_Info_Tab, (0,0))
        screen.blit(Selected, Selected.get_rect(center = (size.w/2, size.h/2)))

        #Blit assets onto the screen
        for item in [Settings, Return, Continue, LengthA, LengthB, LengthC]:
            item.Blit(0,10)
        
        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        if alpha > 225 and Change_Menu == False:
            for button in [Settings, Continue, Return, LengthA, LengthB, LengthC]:
                button.Change_Color(mouse_pos, 0 ,10)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

Load_Config()
In_Game_Menu(-20)
