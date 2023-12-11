import pygame as pg
import json
import sys
import os
from math import sin, radians as rad
from Experiment_Class import *

#You may wonder why i didn't use pygame_menu and yes im asking the same question rn but eh too late
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '0'
pg.display.set_caption("Racing Bet")

pg.mixer.init(48000, -16, 4)

music_channels = pg.mixer.Channel(1)
sfx_channels = pg.mixer.Channel(2)

title_music = pg.mixer.Sound('Assets/music/Forest (rushed ver).wav')
button_click = pg.mixer.Sound('Assets/menu_click.mp3')
interface = pg.mixer.Sound('Assets/interface.mp3')

print(pg.display.get_desktop_sizes())

#Mainly for deleting info when hold backspace
pg.key.set_repeat(600, 25)

#size of current window
size = Screen_Info(screen.get_size())

#mouse animation group
mouse_animation = pg.sprite.Group()    

#FPS event counter
Bg_cycle = pg.USEREVENT + 1
pg.time.set_timer(Bg_cycle, 1000)

#Import 2 Language Files as US and VN
global language
global music_volume
global sfx_volume

def Load_Config():
    global US, VN, language, music_volume, sfx_volume

    with open('locale/en_US.json', 'r', encoding="utf8") as f:
        US = json.load(f)
    with open('locale/vi_VN.json', 'r', encoding="utf8") as f:
        VN = json.load(f)

    try:
        with open ('settings/Config.json', 'r') as f:
            config = json.load(f)
            language = config['Start_Language']
            music_volume = float(config['Music_Volume'])
            sfx_volume = float(config['SFX_Volume'])

    except:
        language = 'US'
        music_volume = 1.0
        sfx_volume = 1.0
    
    sfx_channels.set_volume(sfx_volume)
    music_channels.set_volume(music_volume)

def Shutdown():
    global language, in_full_screen, music_volume, sfx_volume

    save_config = {"Start_Language"     : f"{language}", 
                   "Start_Screen_Size"  : f"{screen.get_size()}",
                   "In_Full_Screen"     : f"{in_full_screen}",
                    "Music_Volume"      : f"{music_volume}",
                    "SFX_Volume"        : f"{sfx_volume}"
                  }

    print(in_full_screen)
    json_file = json.dumps(save_config, indent = 4)
    with open ('settings/Config.json', 'w') as f:
        f.write(json_file)

    pg.quit()
    sys.exit()

def Update_Language(language, menu, name):
    global US
    global VN
    if language == 'US':
        return(f'{US[menu][name]}')
    elif language == 'VN':
        return(f'{VN[menu][name]}')

def Video_Setting(prev_menu, char_set, race_length):
    global in_full_screen
    #For optimization: only call update once when screen size is changed
    change_size = True

    #Set the image of the previous menu as background
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))

    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to different setting menus
                if Audio.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Setting(prev_menu, char_set, race_length)
                if Language.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Setting(prev_menu, char_set, race_length)
                if User_Center.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Setting(prev_menu, char_set, race_length)

                #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    if prev_menu == 'Start Menu':
                        Title_Screen(False)
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, char_set, race_length)
                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, char_set, race_length)
                
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

            #update everything within the menu
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

            _1366x768_text = Font(int(25 * size.w / 1280)).render('1366 x 768', True, '#424769')
            _1280x720_text = Font(int(25 * size.w / 1280)).render('1280 x 720', True, '#424769')

            Video_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Video' ), True, '#424769')
            Audio_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Audio' ), True, '#424769')
            Language_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Language' ), True, '#424769')
            User_Center_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'User_Center' ), True, '#424769')
            Return_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Return' ), True, '#424769')
            Full_Screen_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Video', 'Full_Screen' ), True, '#424769')

        #After all the object has been updated, change the variable to False
        change_size = False

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [Video, Audio, Language, User_Center, Return, Full_Screen, _1366x768, _1280x720]:
            item.Blit()

        #Change colors if the mouse hover above
        for button in [Full_Screen, _1366x768, _1280x720, Audio, Language, User_Center, Return]:
            button.Change_Color(mouse_pos)


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

        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Audio_Setting(prev_menu, char_set, race_length):
    global music_volume
    global sfx_volume
    change_volume_sfx = False
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


    Video_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Video' ), True, '#424769')
    Audio_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Audio' ), True, '#424769')
    Language_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Language' ), True, '#424769')
    User_Center_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'User_Center' ), True, '#424769')
    Return_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Return' ), True, '#424769')
    music_text = Font(int(25*size.w/1280)).render(Update_Language(language, 'Audio', 'Music' ), True, '#FFFFFF')
    sfx_text = Font(int(25*size.w/1280)).render(Update_Language(language, 'Audio', 'SFX' ), True, '#FFFFFF')
    print(music_volume)
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to different setting menus
                if Video.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Setting(prev_menu, char_set, race_length)
                if Language.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Setting(prev_menu, char_set, race_length)
                if User_Center.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Setting(prev_menu, char_set, race_length)

                #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    if prev_menu == 'Start Menu':
                        Title_Screen(False)
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, char_set, race_length)
                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, char_set, race_length)


        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])


        #Blit Assets onto screen
        for item in [Video, Audio, Language, User_Center, Return]:
            item.Blit()

        pg.draw.rect(screen, '#FFFFFF', music_slider, 0, 15)
        pg.draw.rect(screen, '#000000', music_circle, 0, 30)
        pg.draw.rect(screen, '#FFFFFF', sfx_slider, 0, 15)
        pg.draw.rect(screen, '#000000', sfx_circle, 0, 30)

        keys = pg.mouse.get_pressed()
        if music_circle.collidepoint(mouse_pos) and keys[0] == True:
            music_circle.center = (mouse_pos[0], size.h * 0.25)

            if music_circle.left <= music_slider.left: music_circle.left = music_slider.left
            if music_circle.right >= music_slider.right: music_circle.right = music_slider.right

            music_volume = round((music_circle.center[0] - music_slider.midleft[0]) / (300 * size.w/1280), 2)

            if music_volume <= 0.05: music_volume = 0
            if music_volume >= 0.95: music_volume = 1.0

            music_channels.set_volume(music_volume)

        elif sfx_circle.collidepoint(mouse_pos) and keys[0] == True:
            sfx_circle.center = (mouse_pos[0], size.h * 0.4)

            if sfx_circle.left <= sfx_slider.left: sfx_circle.left = sfx_slider.left
            if sfx_circle.right >= sfx_slider.right: sfx_circle.right = sfx_slider.right

            sfx_volume = round((sfx_circle.center[0] - sfx_slider.midleft[0]) / (300 * size.w/1280), 2)

            if sfx_volume <= 0.05: sfx_volume = 0
            if sfx_volume >= 0.95: sfx_volume = 1.0

            sfx_channels.set_volume(sfx_volume)
            
        

        collided = Font(20).render(f"{music_volume}", True, "#FF0000")
        screen.blit(collided, collided.get_rect(center = (size.w/2, size.h/2)))

        #Change colors if the mouse hover above
        for button in [Video, Language, User_Center, Return]:
            button.Change_Color(mouse_pos)
        
        screen.blit(Video_text, Video_text.get_rect(center = (Video.rect.center)))
        screen.blit(Audio_text, Audio_text.get_rect(center = (Audio.rect.center)))
        screen.blit(Language_text, Language_text.get_rect(center = (Language.rect.center)))
        screen.blit(User_Center_text, User_Center_text.get_rect(center = (User_Center.rect.center)))
        screen.blit(Return_text, Return_text.get_rect(center = (Return.rect.center)))

        screen.blit(music_text, music_text.get_rect(midleft = (size.w * 0.35, size.h * 0.25)))
        screen.blit(sfx_text, sfx_text.get_rect(midleft = (size.w * 0.35, size.h * 0.4)))


        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Language_Setting(prev_menu, char_set, race_length):
    global language
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
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                if Choose_US.Mouse_Click(mouse_pos) == True:
                    sfx_channels.play(interface)
                    Change_Language = True
                    language = 'US'
                if Choose_VN.Mouse_Click(mouse_pos) == True:
                    sfx_channels.play(interface)
                    Change_Language = True
                    language = 'VN'

                #Go to different setting menus
                if Video.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Setting(prev_menu, char_set, race_length)
                if Audio.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Setting(prev_menu, char_set, race_length)
                if User_Center.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Setting(prev_menu, char_set, race_length)

                #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    if prev_menu == 'Start Menu':
                        Title_Screen(False)
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, char_set, race_length)
                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, char_set, race_length)

        if Change_Language == True:
            Video_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Video' ), True, '#424769')
            Audio_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Audio' ), True, '#424769')
            Language_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Language' ), True, '#424769')
            User_Center_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'User_Center' ), True, '#424769')
            Return_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Return' ), True, '#424769')


        Change_Language == False
        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [Video, Audio, Language, User_Center, Return, Choose_US, Choose_VN]:
            item.Blit()


        #Change colors if the mouse hover above
        for button in [Video, Audio, User_Center, Return, Choose_US, Choose_VN]:
            button.Change_Color(mouse_pos)

        
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

def User_Center_Setting(prev_menu, char_set, race_length):

    #Load Assets
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))

    Video = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Audio = Button('rect', Video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    Language = Button('rect', Audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    User_Center = Draw_to_Screen('rect', Language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    Return = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    Video_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Video' ), True, '#424769')
    Audio_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Audio' ), True, '#424769')
    Language_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Language' ), True, '#424769')
    User_Center_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'User_Center' ), True, '#424769')
    Return_text = Font(int(25 * size.w / 1280)).render(Update_Language(language, 'Settings', 'Return' ), True, '#424769')

    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to different setting menus
                if Video.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Setting(prev_menu, char_set, race_length)
                if Audio.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Setting(prev_menu, char_set, race_length)
                if Language.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Setting(prev_menu, char_set, race_length)

                    #If return is pressed, return to a previous menu
                if Return.Mouse_Click(mouse_pos):
                    sfx_channels.play(button_click)
                    if prev_menu == 'Start Menu':
                        Title_Screen(False)
                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)
                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, char_set, race_length)
                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, char_set, race_length)


        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', [size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75])
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [Video, Audio, Language, User_Center, Return]:
            item.Blit()


        #Change colors if the mouse hover above
        for button in [Video, Audio, Language, Return]:
            button.Change_Color(mouse_pos)
        
        screen.blit(Video_text, Video_text.get_rect(center = (Video.rect.center)))
        screen.blit(Audio_text, Audio_text.get_rect(center = (Audio.rect.center)))
        screen.blit(Language_text, Language_text.get_rect(center = (Language.rect.center)))
        screen.blit(User_Center_text, User_Center_text.get_rect(center = (User_Center.rect.center)))
        screen.blit(Return_text, Return_text.get_rect(center = (Return.rect.center)))


        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Start_Animation():
    #set the alpha value for the screen (transparency)
    alpha = 250

    #Get logo
    logo = pg.transform.scale(pg.image.load('Assets/icon/Settings/HCMUS_logo.png'), (size.w / 3, size.w / 3))
    logo_rect = logo.get_rect(center = (size.w/2, size.h/2))

    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            #Play mouse animation
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))
            
        screen.fill(0)

        alpha += 1.5
        if alpha < 180 and alpha > 0:
            #show the logo then fade it out shortly afterwards
            logo.set_alpha(int(255 * sin(rad(alpha))))
            screen.blit(logo, logo_rect)

        elif alpha > 250:
            #if alpha then reaches 250, move onto login screen
            mouse_animation.empty()
            Login_Page()

        mouse_animation.update()
        mouse_animation.draw(screen)
        pg.time.Clock().tick(60)
        pg.display.update()

def Login_Page():
    global language
    alpha = 0

    #just stuff for FPS ignore it
    fps = 0
    tru_fps = 0

    #List of valid emails
    valid_emails = ['@gmail.com', '@yahoo.com' , 'End']

    #Login Logics
    username = '' 
    password = ''

    #To know which box the user click (username or password)
    insert = ''

    #Load Assets
    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))

    username_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)

    login_button = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)
    faceID_button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)

    welcome = Font(int(60 * size.w / 1280)).render(Update_Language(language, 'Login', 'Title'), True, '#ffffff')
    login_select = Font(int(20 * size.w / 1280)).render(Update_Language(language,'Login', 'Select_Login'), True, '#d69869')
    signup_select = Button('text', None, None, None, None, Update_Language(language, 'Login', 'Select_Signup'), Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.35, size.h * 0.178))
    username_box_text = Font(int(13 * size.w / 1280)).render(Update_Language(language, 'Login', 'Username_text'), True, '#424769')
    password_box_text = Font(int(13 * size.w / 1280)).render(Update_Language(language, 'Login', 'Password_text'), True, '#424769')
    login_button_text = Font(int(20 * size.w / 1280)).render(Update_Language(language, 'Login', 'Login_Button'), True, '#424769')
    faceID_button_text = Font(int(20 * size.w / 1280)).render(Update_Language(language, 'Login', 'FaceID_Button'), True, '#424769')
    forgot_password = Button('text', None, None, None, None, Update_Language(language, 'Login', 'Forgot_Password'), Font(int(15 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.405, size.h * 0.64))
    login_failed = Font(int(60 * size.w / 1280)).render(Update_Language(language, 'Login', 'Login_Failed'), True, "#FF0000")


    while True:
        alpha -= 2.5
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
                
                #Go to Sign up Page
                if (signup_select.Mouse_Click(mouse_pos)):
                    Signup_Page()

                #To know if user click on username, password box or not
                if username_box.Mouse_Click(mouse_pos):
                    insert = 'username'
                elif password_box.Mouse_Click(mouse_pos):
                    insert = 'password'
                else:
                    insert = ''

                #When user submit Login, check for validity and go to Title Screen if good
                if (login_button.Mouse_Click(mouse_pos)):
                    Title_Screen(True)
                    '''for items in valid_emails:
                        print(username[len(username) - len(items):])
                        if items == 'End':
                            alpha = 300
                            break
                        elif username[len(username) - len(items):] == items:
                            user = User_Data(username, password)
                            if user.Login():
                                Title_Screen()
                            else:
                                alpha = 300

                            break'''


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
        password_input = Font(int(13 * size.w / 1280)).render(password, True, '#FFFFFF')

        #Blit Assets onto the screen
        for item in [signup_select, username_box, password_box, forgot_password, login_button, faceID_button]:
            item.Blit()

        #Change colors if the mouse hover above
        for button in [signup_select, username_box, password_box, login_button, faceID_button, forgot_password]:
            button.Change_Color(mouse_pos)
        
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

def Signup_Page():
    global language

    #just stuff for FPS ignore it
    fps = 0
    tru_fps = 0

    #List of valid emails
    valid_emails = ['@gmail.com', '@yahoo.com' , 'End']

    #Login Logics
    username = '' 
    password = ''
    repeat_password = ''

    #To know which box the user click (username or password)
    insert = ''

    alpha = 0

    #Load Assets
    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))
    
    username_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    password_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    repeat_password_box = Button('rect', (size.w * 0.175, size.h * 0.645), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    
    signup_button = Button('rect', (size.w * 0.175, size.h * 0.775), (size.w*0.275, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)
    signup_button_text = Font(int(30 * size.w / 1280)).render('Sign Up', True, '#424769')

    error = Font(80).render("Password doesn't match", True, "#FF0000")

    welcome = Font(int(60 * size.w / 1280)).render(Update_Language(language, 'Login', 'Title'), True, '#ffffff')
    login_select = Button('text', None, None, None, None, Update_Language(language, 'Sign_Up', 'Select_Login'), Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.265, size.h * 0.178))
    signup_select = Font(int(20 * size.w / 1280)).render(Update_Language(language, 'Sign_Up', 'Select_Signup'), True, '#d69869')
    username_box_text = Font(int(13 * size.w / 1280)).render(Update_Language(language, 'Sign_Up', 'Username_text'), True, '#424769')
    password_box_text = Font(int(13 * size.w / 1280)).render(Update_Language(language, 'Sign_Up', 'Password_text'), True, '#424769')
    signup_button_text = Font(int(20 * size.w / 1280)).render(Update_Language(language, 'Sign_Up', 'Signup_button'), True, '#424769')


    while True:
        alpha -= 5
        fps += 1
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

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

            #Play mouse animation
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_animation.add(Click_Animation(mouse_pos, 5, size.w))

                #Go to Login Page
                if(login_select.Mouse_Click(mouse_pos)):
                    Login_Page()

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
                    if password != repeat_password:
                        error = Font(80).render("Password doesn't match", True, "#FF0000")
                        alpha = 500
                    else:
                        for items in valid_emails:
                            if items == 'End':
                                alpha = 500
                                error = Font(80).render("Invalid username", True, "#FF0000")
                                break
                            elif username[len(username) - len(items):] == items:
                                print('executed')
                                user = User_Data(username, password)
                                user.Sign_Up()
                                Title_Screen(True)
                                break
            #Debug: FPS
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0
        
        screen.fill('#2d3250')
        screen.blit(bg, (size.w*0.125, size.h*0.125))
        pg.draw.rect(screen, '#424769', [size.w*0.125, size.h*0.125, size.w*0.375, size.h * 0.75])

        #Draw the what the user typed in
        username_input = Font(int(12 * size.w / 1280)).render(username, True, '#FFFFFF')
        password_input = Font(int(12 * size.w / 1280)).render(password, True, '#FFFFFF')
        repeat_password_input = Font(int(12 * size.w / 1280)).render(repeat_password, True, '#FFFFFF')

        #Blit Assets onto screen
        for item in [login_select, username_box, password_box, repeat_password_box, signup_button]:
            item.Blit()

        #Change colors if the mouse hover above
        for button in [login_select, username_box, password_box, signup_button, repeat_password_box]:
            button.Change_Color(mouse_pos)

        #Blit Texts onto the screen
        screen.blit(signup_select     ,   signup_select.get_rect(center = (size.w * 0.35, size.h * 0.178)))
        screen.blit(welcome           ,   welcome.get_rect(center = (size.w * 0.3125, size.h * 0.3)))
        screen.blit(username_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.41)))
        screen.blit(password_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.54)))
        screen.blit(signup_button_text ,   signup_button_text.get_rect(center = (signup_button.rect.center)))
        screen.blit(password_box_text ,   username_box_text.get_rect(midleft = (size.w * 0.19, size.h * 0.67)))
        screen.blit(username_input, username_input.get_rect(midleft = (size.w * 0.19, size.h * 0.45)))
        screen.blit(password_input, password_input.get_rect(midleft = (size.w * 0.19, size.h * 0.58)))
        screen.blit(repeat_password_input, repeat_password_input.get_rect(midleft = (size.w * 0.19, size.h * 0.71)))

        #If error then set alpha so message appears then slowly fade away
        error.set_alpha(alpha)
        screen.blit(error, error.get_rect(center = (size.w/2, size.h/2)))

        mouse_animation.update()
        mouse_animation.draw(screen)
        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
        
        pg.time.Clock().tick(60)
        pg.display.update()

def Title_Screen(restart_music):
    fps = 0
    tru_fps = 0
    alpha = 0
    #If enter_game becomes True then stop button functions
    enter_game = False

    if restart_music:
        music_channels.play(title_music, loops = -1)
    #Load Assets
    Background = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert_alpha(), (size.w*1.05, size.h*1.05))
        
    Quit = Button('image', None, None, 'Assets/icon/Settings/shutdown_01.png', (60*size.w/1280, 60* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shutdown_02.png', (size.w * 0.03, size.h * 0.95))

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.97, size.h * 0.05))
    
    #Language Logics
    Prompt = Font(int(25 * size.w/1280)).render(Update_Language(language, 'Title_Screen', 'Prompt'), True, '#000000')

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
                    Video_Setting('Start Menu', '', '')
                
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
            item.Blit()

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
                button.Change_Color(mouse_pos)
        
        mouse_animation.update()
        mouse_animation.draw(screen)
        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))

        pg.time.Clock().tick(60)
        pg.display.update()

def In_Game_Menu(alpha):
    #Mainly for the sake of animation. Target menu is the menu that player selected
    Change_Menu = False
    Target_Menu = ''
    fps = 0
    tru_fps = 0

    #Load Assets
    Background = pg.transform.smoothscale(pg.image.load('Assets/icon/Settings/Cafe.png').convert_alpha(), (512, 288))
    Background = pg.transform.smoothscale(Background, (size.w*1.05, size.h*1.05))

    Settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.97, size.h * 0.05))
    
    Return = Button('image', None, None, 'Assets/icon/Settings/return_01.png', (60*size.w/1280, 60* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/return_02.png', (size.w * 0.03, size.h * 0.95))

    Play = Button('image', None, None, 'Assets/icon/Settings/play.png', (size.w*0.25, size.h * 0.15), None, None, None, None, 'Assets/icon/Settings/play_hover.png', (size.w*0.775, size.h * 0.4))
    Play_Break = pg.transform.scale(pg.image.load('Assets/icon/Settings/play_click.png').convert_alpha(), (size.w*0.3, size.h * 0.2))

    Mini_Game = Button('image', None, None, 'Assets/icon/Settings/minigame.png', (size.w*0.25, size.h * 0.15), None, None, None, None, 'Assets/icon/Settings/minigame_hover.png', (size.w*0.775, size.h * 0.6))
    Mini_Game_CLick = pg.transform.scale(pg.image.load('Assets/icon/Settings/minigame_click.png').convert_alpha(), (size.w*0.3, size.h * 0.2))

    Rank = Button('image', None, None, 'Assets/icon/Settings/rank.png', (size.w*0.25, size.h * 0.15), None, None, None, None, 'Assets/icon/Settings/rank_hover.png', (size.w*0.775, size.h * 0.8))
    Rank_Click = pg.transform.scale(pg.image.load('Assets/icon/Settings/rank_click.png').convert_alpha(), (size.w*0.3, size.h * 0.2))
    
    
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
                        Video_Setting('In_Game_Menu', '', '')
                    
                    #Return to title screen
                    if Return.Mouse_Click(mouse_pos):
                        Title_Screen(True)
            
            #Debug: FPS
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0


        
        screen.fill(0)

        #Background move with cursor
        Bg = Background_Animation(Background, (size.w / 2, size.h / 2), mouse_pos)

        #Fade in animations
        for item in [Background, Settings.image, Play_Break, Play.image, Mini_Game.image, 
                    Mini_Game_CLick, Rank.image, Rank_Click, Return.image]:
            item.set_alpha(alpha)

        Bg.Draw()

        #Load Assets onto screen
        for item in [Play, Mini_Game, Rank, Settings, Return]:
            item.Blit()

        #Fade out animation logics
        if Change_Menu:
            alpha -= 15
            if Target_Menu == 'Play':
                screen.blit(Play_Break, Play_Break.get_rect(center = (Play.rect.center)))
                if alpha < 0:
                    Choose_Character_Set(-20, '', '')
            elif Target_Menu == 'Mini Game':
                screen.blit(Mini_Game_CLick, Mini_Game_CLick.get_rect(center = (Mini_Game.rect.center)))
                if alpha < 0:
                    pass
            elif Target_Menu == 'Rank':
                screen.blit(Rank_Click, Rank_Click.get_rect(center = (Rank.rect.center)))
                if alpha < 0:
                    pass

        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        elif alpha > 225 and Change_Menu == False:
            for button in [Settings, Play, Mini_Game, Rank, Return]:
                button.Change_Color(mouse_pos)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

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
                        Video_Setting('Choose_Character_Set', character_set, race_length)
                    
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
                item.Blit()

        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        if alpha > 225 and Change_Menu == False:
            for button in [Settings, Continue, Return, SetA, SetB, SetC, SetD, SetE]:
                button.Change_Color(mouse_pos)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

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
                        Video_Setting('Choose_Race_Length', character_set, race_length)

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
                item.Blit()
        
        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        if alpha > 225 and Change_Menu == False:
            for button in [Settings, Continue, Return, LengthA, LengthB, LengthC]:
                button.Change_Color(mouse_pos)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        mouse_animation.update()
        mouse_animation.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

Load_Config()
Start_Animation()
