import pygame as pg
import json
import sys
import os
import smtplib
import ssl
import Result_Screen as Result_Screen
from email_validator import validate_email
from email.message import EmailMessage
from math import sin, radians as rad
from Experiment_Class import *
from random import randint, randrange, uniform, choice

os.environ['SDL_VIDEO_CENTERED'] = '0'
pg.display.set_caption("Racing Bet")

#music playback
pg.mixer.init(48000, -16, 4)

music_channels = pg.mixer.Channel(1)
sfx_channels = pg.mixer.Channel(2)

title_music = pg.mixer.Sound('Assets/music/Forest (rushed ver).wav')
button_click = pg.mixer.Sound('Assets/menu_click.mp3')
interface = pg.mixer.Sound('Assets/interface.mp3')

#For holding down Backspace
pg.key.set_repeat(600, 25)

#size of current screen
size = Screen_Info(screen.get_size())

#mouse animation group
click_ani = pg.sprite.Group()

#FPS event counter
Bg_cycle = pg.USEREVENT + 1
pg.time.set_timer(Bg_cycle, 1000)

#Create instance of user
current_user = User_Data()

#Load the config (lang, volume)
def Load_Config():
    global US, VN, lang, music_volume, sfx_volume

    #open config files
    with open('locale/en_US.json', 'r', encoding = "utf8") as f:
        US = json.load(f)

    with open('locale/vi_VN.json', 'r', encoding = "utf8") as f:
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
def Send_Email(email):
    #Get pwd (private reason ehe)
    #with open ("C:/Users/ADMIN/Desktop/app.txt", 'r') as f:
        #pwd = f.read()
    
    pwd = 'owpp kuca jmfy qwcm'
    
    #Get sender and receiver
    sender = "mihikoxakamatsu@gmail.com"
    receiver = email

    #Generate code
    code = randint(100000, 999999)

    #Email content
    Title = "Email Verifications for School Project"

    Body = f"""
    Your email verification code is: {code}
        
    Please ignore this email if it is mistakenly sent to you."""
    
    #Encode
    code = hashlib.sha256(str(code).encode()).hexdigest()

    #Making the emails
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = Title
    em.set_content(Body)

    context = ssl.create_default_context()

    #Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, pwd)
        smtp.sendmail(sender, receiver, em.as_string())

    #return to compare with user input
    return code

#Logo Animation
def Start_Animation():
    #set the alpha value for the screen
    alpha = 250

    #Get logo
    logo = pg.transform.scale(pg.image.load('Assets/icon/Settings/HCMUS_logo.png'), (size.w / 3, size.w / 3))
    logo_rect = logo.get_rect(center = (size.w/2, size.h/2))

    #Main code
    while True:
        alpha += 1.5
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            #Play mouse animation
            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))
            
        #Code
        screen.fill(0)

        if alpha < 180 and alpha > 0:
            #show the logo then fade it out shortly afterwards
            logo.set_alpha(int(255 * sin(rad(alpha))))
            screen.blit(logo, logo_rect)

        elif alpha > 250:
            #if alpha then reaches 250, move onto login screen
            Login('', '')


        click_ani.update()
        click_ani.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

#Login
def Login(email, pwd):
    alpha = 0

    #To know which box the user click (email or pwd)
    insert = ''

    #Load Assets
    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))
    bounding_box = pg.rect.Rect((0,0), (size.w*0.275, size.h * 0.1))

    to_signup = Button('text', None, None, None, None, Updt_Lang(lang, 'Login', 'To_Signup'), 
                           Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.35, size.h * 0.178))
    
    forgot_pwd = Button('text', None, None, None, None, Updt_Lang(lang, 'Login', 'Forgot_Pwd'), 
                            Font(int(15 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.405, size.h * 0.64))

    email_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), 
                          None, None, None, None, '#676f9d', '#5d648c', None, None)
    
    pwd_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), 
                          None, None, None, None, '#676f9d', '#5d648c', None, None)

    submit_login = Button('rect', (size.w * 0.175, size.h * 0.7), (size.w*0.1, size.h * 0.06), 
                          None, None, None, None, '#f9b17a', '#d69869', None,  None)
    
    faceID_button = Button('rect', (size.w * 0.345, size.h * 0.7), (size.w*0.1, size.h * 0.06), 
                           None, None, None, None, '#f9b17a', '#d69869', None,  None)

    quit = Button('image', None, None, 'Assets/icon/Settings/shutdown_01.png', (50*size.w/1280, 50* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shutdown_02.png', (size.w * 0.025, size.h * 0.955))
    

    welcome =       Font(int(60 * size.w / 1280)).render (Updt_Lang(lang, 'Login', 'Title'), True, '#ffffff')
    to_login =      Font(int(20 * size.w / 1280)).render(Updt_Lang(lang,'Login', 'To_Login'), True, '#d69869')
    email_txt =     Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Email_Txt'), True, '#424769')
    pwd_txt =       Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Pwd_Txt'), True, '#424769')
    login_txt =     Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Submit_Login'), True, '#424769')
    faceID_txt =    Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'FaceID_Btn'), True, '#424769')

    login_failed = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Login_Failed'), True, "#FF0000")

    while True:
        alpha -= 7.5
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.KEYDOWN:
                
                #User clicked email
                if insert == 'email':
                    if event.key == pg.K_BACKSPACE:

                        email = email[:-1]
                    else:
                        email += event.unicode

                #User clicked pwd
                elif insert == 'pwd':
                    if event.key == pg.K_BACKSPACE:
                        pwd = pwd[:-1]
                    else:
                        pwd += event.unicode

            if event.type == pg.MOUSEBUTTONDOWN:
                #Play mouse animation
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                if quit.Click(mouse_pos):
                    Shutdown()
                
                #Go to Sign up Page
                if (to_signup.Click(mouse_pos)):
                    Signup('', '')

                #To know if user click on email, pwd box or not
                if email_box.Click(mouse_pos):
                    insert = 'email'
                elif pwd_box.Click(mouse_pos):
                    insert = 'pwd'
                else:
                    insert = ''

                #When user submit Login, check for validity and go to Title Screen if good
                if (submit_login.Click(mouse_pos)):
                    print(pwd)
                    current_user.email = email
                    current_user.pwd = hashlib.sha256(pwd.encode()).hexdigest()
                    if current_user.Login():
                        print(current_user.email)
                        Title(True)
                    else:
                        alpha = 500

        screen.fill('#2d3250')
        screen.blit(bg, (size.w*0.125, size.h*0.125))
        pg.draw.rect(screen, '#424769', [size.w*0.125, size.h*0.125, size.w*0.375, size.h * 0.75])

        #Blit Assets onto the screen
        for item in [to_signup, email_box, pwd_box, forgot_pwd, submit_login, faceID_button, quit]:
            item.Blit(0,10)
            item.Hover(mouse_pos, 0 ,10)

        #Draw the what the user typed in
        email_input = Font(int(13 * size.w / 1280)).render(email, True, '#FFFFFF')
        pwd_input = Font(int(13 * size.w / 1280)).render((len(pwd)) * '*', True, '#FFFFFF')
        
        #Blit Texts onto the screen
        screen.blit(to_login   ,    to_login.get_rect(center = (size.w * 0.265, size.h * 0.178)))
        screen.blit(welcome    ,    welcome.get_rect(center = (size.w * 0.3125, size.h * 0.3)))
        screen.blit(email_txt  ,    email_txt.get_rect(midleft = (size.w * 0.19, size.h * 0.41)))
        screen.blit(pwd_txt    ,    email_txt.get_rect(midleft = (size.w * 0.19, size.h * 0.54)))
        screen.blit(login_txt  ,    login_txt.get_rect(center = (submit_login.rect.center)))
        screen.blit(faceID_txt ,    faceID_txt.get_rect(center = (faceID_button.rect.center)))
        screen.blit(email_input,    email_input.get_rect(midleft = (size.w * 0.19, size.h * 0.45)))
        screen.blit(pwd_input  ,    pwd_input.get_rect(midleft = (size.w * 0.19, size.h * 0.58)))

        if insert == 'email':
            bounding_box.center = email_box.rect.center
            pg.draw.rect(screen, '#FFFFFF', bounding_box, 2, 10)
        elif insert == 'pwd':
            bounding_box.center = pwd_box.rect.center
            pg.draw.rect(screen, '#FFFFFF', bounding_box, 2, 10)
        
        #If error then set alpha so message appears then slowly fade away
        login_failed.set_alpha(alpha)
        screen.blit(login_failed, login_failed.get_rect(center = (size.w/2, size.h/2)))

        click_ani.update()
        click_ani.draw(screen)
        pg.time.Clock().tick(60)
        pg.display.update()

#Sign up
def Signup(email, pwd):
    global lang
    #Login Logics
    repeat_pwd = pwd

    #To know which box the user click (email or pwd)
    insert = ''

    pwd_mismatch_alpha = 0
    pwd_len_error_alpha = 0
    email_alpha = 0
    existed_alpha = 0

    #Load Assets
    bg = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert(), (size.w*0.75, size.h*0.75))
    bounding_box = pg.rect.Rect((0,0), (size.w*0.275, size.h * 0.1))
    
    email_box = Button('rect', (size.w * 0.175, size.h * 0.385), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    pwd_box = Button('rect', (size.w * 0.175, size.h * 0.515), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    repeat_pwd_box = Button('rect', (size.w * 0.175, size.h * 0.645), (size.w*0.275, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    
    submit_signup = Button('rect', (size.w * 0.175, size.h * 0.775), (size.w*0.275, size.h * 0.06), None, None, None, None, '#f9b17a', '#d69869', None,  None)

    to_login = Button('text', None, None, None, None, Updt_Lang(lang, 'Sign_Up', 'To_Login'), Font(int(20 * size.w / 1280)), '#676f9d', '#5d648c', None, (size.w * 0.265, size.h * 0.178))

    Quit = Button('image', None, None, 'Assets/icon/Settings/shutdown_01.png', (50*size.w/1280, 50* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shutdown_02.png', (size.w * 0.025, size.h * 0.955))

    welcome = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Login', 'Title'), True, '#ffffff')
    to_signup = Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'To_Signup'), True, '#d69869')
    email_txt = Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Email_Txt'), True, '#424769')
    pwd_txt = Font(int(13 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Pwd_Txt'), True, '#424769')
    repeat_pwd_txt = Font(int(13 * size.w/1280)).render(Updt_Lang(lang, 'Sign_Up', 'Repeat_Pwd_Txt'), True, "#424769")
    submit_signup_txt = Font(int(20 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Submit_Signup'), True, '#424769')

    email_error = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Email_Error'), True, "#FF0000")
    pwd_mismatch = Font(int(60 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Pwd_Mismatch'), True, "#FF0000")
    pwd_len_error = Font(int(50 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Pwd_Len_Error'), True, "#FF0000")
    existed_error = Font(int(50 * size.w / 1280)).render(Updt_Lang(lang, 'Sign_Up', 'Existed'), True, "#FF0000")


    while True:
        email_alpha -= 7.5
        pwd_mismatch_alpha -= 7.5
        pwd_len_error_alpha -= 7.5
        existed_alpha -= 7.5

        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            #Play mouse animation
            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                if Quit.Click(mouse_pos):
                    Shutdown()

                #Go to Login Page
                if(to_login.Click(mouse_pos)):
                    Login('', '')

                #To know which box user clicked
                if email_box.Click(mouse_pos):
                    insert = 'email'
                elif pwd_box.Click(mouse_pos):
                    insert = 'pwd'
                elif repeat_pwd_box.Click(mouse_pos):
                    insert = 'repeat_pwd'
                else:
                    insert = ''

                #When user submit Sign up, check for validity and go to Title Screen if good
                if submit_signup.Click(mouse_pos):
                    
                    if len(pwd) < 8:
                        pwd_len_error_alpha = 500
                    elif pwd != repeat_pwd:
                        pwd_mismatch_alpha = 500
                    elif (current_user.Sign_Up_Validate() == False):
                        existed_alpha = 500
                    elif (Validate_Email(email) == False):
                        email_alpha = 500
                    else :
                        current_user.email = email
                        current_user.pwd = hashlib.sha256(pwd.encode()).hexdigest()
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Enter_Code(email, pwd, Send_Email(email))

            
            if event.type == pg.KEYDOWN:
                #User clicked email
                if insert == 'email':
                    if event.key == pg.K_BACKSPACE:
                        email = email[:-1]
                    else:
                        email += event.unicode
                        
                #User clicked pwd
                elif insert == 'pwd':
                    if event.key == pg.K_BACKSPACE:
                        pwd = pwd[:-1]
                    else:
                        pwd += event.unicode

                #User clicked re-enter pwd
                elif insert == 'repeat_pwd':
                    if event.key == pg.K_BACKSPACE:
                        repeat_pwd = repeat_pwd[:-1]
                    else:
                        repeat_pwd += event.unicode

        screen.fill('#2d3250')
        screen.blit(bg, (size.w*0.125, size.h*0.125))
        pg.draw.rect(screen, '#424769', [size.w*0.125, size.h*0.125, size.w*0.375, size.h * 0.75])

        #Draw the what the user typed in
        email_input = Font(int(12 * size.w / 1280)).render(email, True, '#FFFFFF')
        pwd_input = Font(int(12 * size.w / 1280)).render(len(pwd) * '*', True, '#FFFFFF')
        repeat_pwd_input = Font(int(12 * size.w / 1280)).render(len(repeat_pwd) * '*', True, '#FFFFFF')

        #Blit Assets onto screen
        for item in [to_login, email_box, pwd_box, repeat_pwd_box, submit_signup, Quit]:
            item.Blit(0,10)
            item.Hover(mouse_pos, 0 ,10)

        #Blit Texts onto the screen
        screen.blit(to_signup        ,     to_signup.get_rect(center = (size.w * 0.35, size.h * 0.178)))
        screen.blit(welcome          ,     welcome.get_rect(center = (size.w * 0.3125, size.h * 0.3)))
        screen.blit(email_txt        ,     email_txt.get_rect(midleft = (size.w * 0.19, size.h * 0.41)))
        screen.blit(pwd_txt          ,     email_txt.get_rect(midleft = (size.w * 0.19, size.h * 0.54)))
        screen.blit(repeat_pwd_txt   ,     repeat_pwd_txt.get_rect(midleft = (size.w * 0.19, size.h * 0.67)))
        screen.blit(submit_signup_txt,     submit_signup_txt.get_rect(center = (submit_signup.rect.center)))
        screen.blit(email_input      ,     email_input.get_rect(midleft = (size.w * 0.19, size.h * 0.45)))
        screen.blit(pwd_input        ,     pwd_input.get_rect(midleft = (size.w * 0.19, size.h * 0.58)))
        screen.blit(repeat_pwd_input ,     repeat_pwd_input.get_rect(midleft = (size.w * 0.19, size.h * 0.71)))

        match insert:
            case 'email':
                bounding_box.center = email_box.rect.center
                pg.draw.rect(screen, '#FFFFFF', bounding_box, 2, 10)
            case 'pwd':
                bounding_box.center = pwd_box.rect.center
                pg.draw.rect(screen, '#FFFFFF', bounding_box, 2, 10)
            case 'repeat_pwd':
                bounding_box.center = repeat_pwd_box.rect.center
                pg.draw.rect(screen, '#FFFFFF', bounding_box, 2, 10)

        #If error then set alpha so message appears then slowly fade away
        email_error.set_alpha(email_alpha)
        pwd_mismatch.set_alpha(pwd_mismatch_alpha)
        pwd_len_error.set_alpha(pwd_len_error_alpha)
        existed_error.set_alpha(existed_alpha)

        for item in [email_error, pwd_mismatch, pwd_len_error, existed_error]:
            screen.blit(item, item.get_rect(center = (size.w/2, size.h/2)))
        
        click_ani.update()
        click_ani.draw(screen)    
        pg.time.Clock().tick(60)
        pg.display.update()

#Enter confirmation code
def Enter_Code(email, pwd, en_code):
    insert = False
    verify_code = ''
    error_alpha = 0

    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg.convert(), (size.w, size.h))

    bounding_box = pg.rect.Rect((0,0), (size.w*0.45, size.h * 0.15))

    box = pg.rect.Rect((0,0) , (size.w * 0.6, size.h * 0.6))
    box.center = (size.w * 0.5, size.h * 0.5)

    box_outline = pg.rect.Rect((0,0) , (size.w * 0.6005, size.h * 0.6005))
    box_outline.center = (size.w * 0.5, size.h * 0.5)

    title = Font(int(60*size.w/1280)).render(Updt_Lang(lang, 'Enter_Code', 'Title'), True, "#FFFFFF")
    prompt = Font(int(20*size.w/1280)).render(Updt_Lang(lang, 'Enter_Code', 'Prompt'), True, '#FFFFFF')
    
    verify = Button('rect', (0,0), (size.w*0.45, size.h * 0.15), None, None, None, None, '#676f9d', '#5d648c', None, None)
    verify.rect.center = (size.w * 0.5, size.h * 0.525)
    verify_text = Font(int(15*size.w/1280)).render(Updt_Lang(lang, 'Enter_Code', 'Box_Txt'), True, '#424769')

    submit = Button('rect', (0,0), (size.w*0.125, size.h * 0.07), None, None, None, None, '#f9b17a', '#d69869', None, None)
    submit.rect.center = (size.w * 0.5, size.h * 0.6875)
    submit_text = Font(int(20*size.w/1280)).render(Updt_Lang(lang, 'Enter_Code', 'Submit'), True, '#424769')

    close = Button('image', None, None, 'Assets/Obstacles/frame_box.png', (48*size.w/1280, 48*size.w/1280), None, None, None, None , 'Assets/Obstacles/frame_box.png', (0,0))
    close.rect.center = box_outline.topright

    wrong_code = Font(int(60*size.w/1280)).render(Updt_Lang(lang, 'Enter_Code', 'Error'), True, '#FF0000')

     
    while True:
        error_alpha -= 7.5
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Go to Login Page

                if verify.Click(mouse_pos):
                    insert = True
                else:
                    insert = False
                
                if close.Click(mouse_pos):
                    Signup(email, pwd)
                
                if submit.Click(mouse_pos):
                    if hashlib.sha256(verify_code.encode()).hexdigest() == en_code:
                        current_user.email = email
                        current_user.pwd = hashlib.sha256(pwd.encode()).hexdigest()
                        current_user.Sign_Up()
                        Enter_Username('Sign Up', None, None, None)
                        
                    else:
                        error_alpha = 500

            if event.type == pg.KEYDOWN:
                if insert:
                    if event.key == pg.K_BACKSPACE:
                        verify_code = verify_code[:-1]
                    else:
                        verify_code += event.unicode
        
        screen.fill(0)
        screen.blit(bg, (0,0))
        enter_verify_text = Font(int(50*size.w/1280)).render(verify_code, True, '#FFFFFF')

        pg.draw.rect(screen, '#424769', box, 0, 10)
        pg.draw.rect(screen, '#000000', box_outline, 5, 10)

        for item in [verify, submit, close]:
            item.Blit(0,10)
            item.Hover(mouse_pos, 0, 10)

        screen.blit(enter_verify_text, enter_verify_text.get_rect(center = (verify.rect.center)))
        screen.blit(title, title.get_rect(center = (size.w/2, size.h * 0.325)))
        screen.blit(prompt, prompt.get_rect(center = (size.w/2, size.h * 0.385)))
        screen.blit(submit_text, submit_text.get_rect(center = (submit.rect.center)))

        if (insert == False and verify_code == ''):
            screen.blit(verify_text, verify_text.get_rect(center = (verify.rect.center)))
        else:
            bounding_box.center = verify.rect.center
            pg.draw.rect(screen, "#FFFFFF", bounding_box, 5, 10)
        
        wrong_code.set_alpha(error_alpha)
        screen.blit(wrong_code, wrong_code.get_rect(center = (submit.rect.center)))

        click_ani.update()
        click_ani.draw(screen)
        pg.time.Clock().tick(60)
        pg.display.update()

def Enter_Username(before, prev_menu, set_char, race_len):
    insert = False
    username = ''
    username_error_alpha = 0

    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg.convert(), (size.w, size.h))

    bounding_box = pg.rect.Rect((0,0), (size.w*0.45, size.h * 0.15))

    title = Font(int(60*size.w/1280)).render(Updt_Lang(lang, 'Enter_Username', 'Title'), True, "#FFFFFF")

    box = pg.rect.Rect((0,0) , (size.w * 0.6, size.h * 0.6))
    box.center = (size.w * 0.5, size.h * 0.5)
    box_outline = pg.rect.Rect((0,0) , (size.w * 0.6005, size.h * 0.6005))
    box_outline.center = box.center
    
    verify = Button('rect', (0,0), (size.w*0.45, size.h * 0.15), None, None, None, None, '#676f9d', '#5d648c', None, None)
    verify.rect.center = (size.w * 0.5, size.h * 0.525)
    verify_text = Font(int(20*size.w/1280)).render(Updt_Lang(lang, 'Enter_Username', 'Box_Txt'), True, '#424769')

    submit = Button('rect', (0,0), (size.w*0.125, size.h * 0.07), None, None, None, None, '#f9b17a', '#d69869', None, None)
    submit.rect.center = (size.w * 0.5, size.h * 0.6875)
    submit_text = Font(int(20*size.w/1280)).render(Updt_Lang(lang, 'Enter_Username', 'Submit'), True, '#424769')

    close = Button('image', None, None, 'Assets/icon/Settings/close.png', (40*size.w/1280, 40*size.w/1280), None, None, None, None , 'Assets/icon/Settings/close-1.png', (0,0))
    close.rect.center = box_outline.topright

    username_error = Font(int(60 * size.w / 1280)).render("Username can't be empty", True, "#FF0000")
     
    while True:
        mouse_pos = pg.mouse.get_pos()
        username_error_alpha -= 7.5

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Go to Login Page
                if(verify.Click(mouse_pos)):
                    insert = True
                else:
                    insert = False
                
                if (submit.Click(mouse_pos)):
                    if username == '':
                        username_error_alpha = 500
                    else:
                        current_user.username = username
                        current_user.Update_Username(username)
                        if before == 'Sign Up':
                            Title(True)
                        if before == 'Settings':
                            User_Center_Menu(prev_menu, set_char, race_len)

                if close.Click(mouse_pos) and before == 'Settings':
                    User_Center_Menu(prev_menu, set_char, race_len)

            if event.type == pg.KEYDOWN:
                if insert:
                    if event.key == pg.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
        
        screen.fill(0)
        screen.blit(bg, (0,0))
        username_txt = Font(int(50*size.w/1280)).render(username, True, '#FFFFFF')

        pg.draw.rect(screen, '#424769', box, 0, 10)
        pg.draw.rect(screen, '#000000', box_outline, 5, 10)

        for item in [verify, submit]:
            item.Blit(0,10)
            item.Hover(mouse_pos, 0, 10)
        
        if before == 'Settings':
            close.Blit(0,10)
            close.Hover(mouse_pos, 0,10)

        screen.blit(username_txt, username_txt.get_rect(center = (verify.rect.center)))
        screen.blit(title, title.get_rect(center = (size.w/2, size.h * 0.325)))
        screen.blit(submit_text, submit_text.get_rect(center = (submit.rect.center)))

        if (insert == False and username == ''):
            screen.blit(verify_text, verify_text.get_rect(center = (verify.rect.center)))
        else:
            bounding_box.center = verify.rect.center
            pg.draw.rect(screen, "#FFFFFF", bounding_box, 5, 10)

        username_error.set_alpha(username_error_alpha)
        screen.blit(username_error, username_error.get_rect(center = (size.w/2, size.h/2)))

        click_ani.update()
        click_ani.draw(screen)
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
    background = pg.transform.scale(pg.image.load('Assets/background/village/village.png').convert_alpha(), (size.w*1.075, size.h*1.075))
        
    quit = Button('image', None, None, 'Assets/icon/Settings/shutdown_01.png', (50*size.w/1280, 50* size.w/1280), 
                None, None, None, None, 'Assets/icon/Settings/shutdown_02.png', (size.w * 0.025, size.h * 0.955))

    settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (50*size.w/1280, 50* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.975, size.h * 0.045))
    
    title = Font(int(100 * size.w / 1280)).render('Racing Bet', True, "#000000")
    prompt = Font(int(25 * size.w/1280)).render(Updt_Lang(lang, 'Title', 'Prompt'), True, '#000000')

    while True:
        alpha += 5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #If Quit button is pressed, exit the game only when enter_game is False
                if quit.Click(mouse_pos) == True and enter_game == False:
                    Shutdown()
                
                #Go to Settings Page
                if (settings.Click(mouse_pos) == True and enter_game == False):
                    sfx_channels.play(button_click)
                    pg.image.save(screen, 'Assets/temps/temp.png')
                    Video_Menu('Title', '', '')
                
                #If user click anywhere on the screen, set alpha to 255 and enter_game = True to stop all button function
                elif enter_game == False:
                    enter_game = True
                    alpha = 255

            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0
        
        #Base
        screen.fill(0)

        #Background moves with cursor
        bg = Bg_Ani(background, (size.w / 2, size.h / 2), mouse_pos)

        #Set alpha for fade in animation
        for item in [settings.image, quit.image, bg.image, title, prompt]:
            item.set_alpha(alpha)

        #Make the prompt continuously flashing
        prompt.set_alpha(255 * abs(sin(rad(alpha))))
        bg.Draw()

        #Blit Assets onto screen
        for item in  [quit, settings]:
            item.Blit(0,10)

        screen.blit(title, title.get_rect(center = (size.w * 0.5, size.h *0.25 )))
        screen.blit(prompt, prompt.get_rect(center = (size.w * 0.5, size.h * 0.75)))

        #Fade out animaion
        if enter_game:
            alpha -= 15
            if alpha < -20: In_Game_Menu(255)     
        else:
            for button in [quit, settings]:
                button.Hover(mouse_pos, 0 ,10)
        

        click_ani.update()
        click_ani.draw(screen)

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))

        pg.time.Clock().tick(60)
        pg.display.update()

#In Game Screen
def In_Game_Menu(alpha):
    #Mainly for the sake of animation. Target menu is the menu that player selected
    change_menu = False
    target_menu = ''
    fps = 0
    tru_fps = 0
    minigame_error_alpha = 0
    play_error_alpha = 0

    #Load Assets
    background = pg.transform.smoothscale(pg.image.load('Assets/in_game_bg.png').convert_alpha(), (size.w*1.075, size.h*1.075))

    settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (50*size.w/1280, 50* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.975, size.h * 0.045))

    play = Button('rect', (0,0), ((size.w*0.25, size.h * 0.15)), None, None, None, None, '#676f9d', '#5d648c', None, None)
    play.rect.center = (size.w*0.775, size.h * 0.4)

    mini_Game = Button('rect', (0,0), ((size.w*0.25, size.h * 0.15)), None, None, None, None, '#676f9d', '#5d648c', None, None)
    mini_Game.rect.center = (size.w*0.775, size.h * 0.6)

    history = Button('rect', (0,0), ((size.w*0.25, size.h * 0.15)), None, None, None, None, '#676f9d', '#5d648c', None, None)
    history.rect.center = (size.w*0.775, size.h * 0.8)

    ani_surf = pg.surface.Surface((size.w, size.h))
    ani_surf.fill('#000000')
    

    #coins_box = pg.rect.Rect((0,0), ((size.w*0.25, size.h * 0.25)))
    #coins_box.center = ((size.w*0.275, size.h * 0.5))

    coins_img = pg.image.load('Assets/coin.png').convert_alpha()
    coins_img = pg.transform.rotozoom(coins_img, 0, 3.5)

    coins_Text = Font(int(60*size.w/1280)).render(f'{current_user.coin}', True, "#FFFFFF")
    username_text = Font(int(60 * size.w /1280)).render(f'Hello, {current_user.username}', True, '#FFFFFF')

    minigame_error = Font(int(40 * size.w/1280)).render("You have enough coin, can't enter minigame", True, '#FF0000')
    play_error = Font(int(40 * size.w/1280)).render("You don't have enough coin. Play minigame for more", True, '#FF0000')

    while True:
        alpha -= 7.5
        minigame_error_alpha -= 7.5
        play_error_alpha -= 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Set the alpha for fade out animation when user click on a menu
                if change_menu == False:
                    if play.Click(mouse_pos):
                        if current_user.coin < 200:
                            play_error_alpha = 500
                        else:
                            change_menu = True
                            target_menu = 'Play'

                    if mini_Game.Click(mouse_pos):
                        if current_user.coin >= 200:
                            minigame_error_alpha = 500
                        else:
                            change_menu = True
                            target_menu = 'Mini Game'

                    if history.Click(mouse_pos):
                        change_menu = True
                        target_menu = 'History'
                        pg.image.save(screen, 'Assets/temps/temp.png')

                    #Go to Settings Page
                    if settings.Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Menu('In_Game_Menu', '', '')
            
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                print(True)
                current_user.Update_Coin(1)
            #Debug: FPS
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        
        screen.fill(0)
        #Background move with cursor
        bg = Bg_Ani(background, (size.w / 2, size.h / 2), mouse_pos)
        bg.Draw()

        #Load Assets onto screen
        for item in [play, mini_Game, history, settings]:
            item.Blit(0,10)

        #pg.draw.rect(screen, "#FFFFFF", coins_box, 2, 10)

        screen.blit(coins_img, coins_img.get_rect(midleft = (size.w*0.125, size.h * 0.575)))
        screen.blit(username_text, username_text.get_rect(midleft = (size.w*0.125, size.h * 0.45)))
        screen.blit(coins_Text, coins_Text.get_rect(midleft = (size.w*0.175, size.h * 0.575)))

        minigame_error.set_alpha(minigame_error_alpha)
        screen.blit(minigame_error, minigame_error.get_rect(center = (size.w/2, size.h/2)))

        play_error.set_alpha(play_error_alpha)
        screen.blit(play_error, play_error.get_rect(center = (size.w/2, size.h/2)))

        print(alpha)

        if alpha <= 0: alpha = 0
        ani_surf.set_alpha(alpha)
        screen.blit(ani_surf, (0,0))
        
        
        #Fade out animation logics
        if change_menu:
            alpha += 15
            if alpha > 256:
                if target_menu == 'Play':
                    Choose_Character_Set(-20, 5, 3)

                elif target_menu == 'Mini Game':
                    Mini_Game_Menu()

                elif target_menu == 'History':
                    History_Menu()

        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        elif alpha == 0 and change_menu == False:
            for button in [settings, play, mini_Game, history]:
                button.Hover(mouse_pos, 0 ,10)
        

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        click_ani.update()
        click_ani.draw(screen)

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
                if self.pre_score % 4 == 0:
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
                            if ado_dino.rect.bottom == int(0.98 * size.h):
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
                    current_user.Update_Coin(gold)
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
                    text = Font(int(100 * size.w / 1280)).render("GAME OVER", True, (0, 0, 0))
                    score = Font(int(30 * size.w / 1280)).render("Your gold      : " + str(gold), True, (0, 0, 0))
                    scoreRect = score.get_rect()
                    scoreRect.center = (size.w * 0.5, size.h * 0.4)
                    SCREEN.blit(score, scoreRect)
                    textRect = text.get_rect()
                    textRect.center = (size.w * 0.5, size.h * 0.25)
                    SCREEN.blit(text, textRect)
                    SCREEN.blit(coin_symbol,(675 * size.w / 1280 , 277 * size.w /1280))
                    prompt = Font(int(20 * size.w / 1280)).render("- Press ESC to return to main menu -", True, "#000000")
                    SCREEN.blit(prompt, prompt.get_rect(center = (size.w/2, size.h* 0.6)))
                    pg.display.update()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            Shutdown()
                        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                            In_Game_Menu(-20)

                    time_clock.tick(FPS)
                
        pg.quit()
        quit()

    def main():
        isGameQuit = introduction_screen()
        if not isGameQuit:
            gameplay()

    main()

def History_Menu():
    win = None
    coin = None
    chr_set = None
    race_len = None

    background = pg.transform.smoothscale(pg.image.load('Assets/in_game_bg.png').convert_alpha(), (512, 288))
    background = pg.transform.smoothscale(background, (size.w*1.075, size.h*1.075))

    title = Font(60).render(Updt_Lang(lang, 'History', 'Title'), True, "#FFFFFF")

    #prompt = Font(20).render(Updt_Lang(lang, 'History', 'Prompt'), True, "#FFFFFF")

    add_record = Button('rect', (0,0), (size.w * 0.25, size.h * 0.1), None, None, None, None, '#000000', '#FFFFFF', None, None)
    add_record.rect.center = (size.w/2, size.h/4)
    add_record_Txt = Font(40).render('Add Record', True, "#00FF00")

    box = pg.rect.Rect((0,0), (size.w * 0.75, size.h * 0.9))
    box.center = (size.w/2, size.h/2)

    box_outline = pg.rect.Rect((0,0), (size.w * 0.75, size.h * 0.9))
    box_outline.center = (size.w/2, size.h/2)

    chr_Set = Font(30).render("Selected Set", True, "#FFFFFF")
    race_Len = Font(30).render("Race Length", True, "#FFFFFF")
    result = Font(30).render("Result", True, "#FFFFFF")
    coins_Change = Font(30).render("Coin Gained", True, "#FFFFFF")

    empty = Font(30).render(Updt_Lang(lang, 'History', 'Empty'), True, "#FFFFFF")
    close = Button('image', None, None, 'Assets/icon/Settings/close.png', (40*size.w/1280, 40*size.w/1280), None, None, None, None , 'Assets/icon/Settings/close-1.png', (0,0))
    close.rect.center = box_outline.topright


    while True:
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))
                if add_record.Click(mouse_pos):
                    win = randrange(0,2)
                    coin = randrange(-200, 200)
                    chr_set = randrange(0,5)
                    race_len = randrange(0,3)
                    current_user.Save_History(chr_set, race_len, win, coin)
                
                if close.Click(mouse_pos):
                        In_Game_Menu(-20)

              
        screen.blit(background, (0,0))
        pg.draw.rect(screen, '#424769', box, 0 , 10)
        pg.draw.rect(screen, '#000000', box_outline, 5 , 10)

        for item in [close]:
            item.Blit(0,0)
            item.Hover(mouse_pos, 0, 0)

        if len(current_user.Get_History()) == 0:
            screen.blit(empty, empty.get_rect(center = (size.w/2, size.h * 0.35)))

        else:
            for i in range(0, len(current_user.Get_History())):
                history_id = Game_History(current_user.Get_History()[i], lang, size.w)
                history_id.chr_set_rect.center = (size.w * 0.25, size.h * 0.275 + size.h * 0.1 * (i+1))
                history_id.race_len_rect.center = (size.w * 0.416, size.h * 0.275 + size.h* 0.1 * (i+1))
                history_id.result_rect.center = (size.w * 0.583, size.h * 0.275 + size.h* 0.1 * (i+1))
                history_id.coins_change_rect.center = (size.w * 0.75, size.h * 0.275 + size.h* 0.1 * (i+1))

                screen.blit(history_id.chr_set, history_id.chr_set_rect)
                screen.blit(history_id.race_len, history_id.race_len_rect)
                screen.blit(history_id.result, history_id.result_rect)
                screen.blit(history_id.coins_change, history_id.coins_change_rect)


        screen.blit(title, title.get_rect(center = (size.w * 0.5, size.h * 0.15)))
        #screen.blit(prompt, prompt.get_rect(center = (size.w * 0.5, size.h * 0.225)))

        screen.blit(chr_Set, chr_Set.get_rect(center = (size.w * 0.25, size.h * 0.275)))
        screen.blit(race_Len, race_Len.get_rect(center = (size.w * 0.416, size.h * 0.275)))
        screen.blit(result, result.get_rect(center = (size.w * 0.583, size.h * 0.275)))
        screen.blit(coins_Change, coins_Change.get_rect(center = (size.w * 0.75, size.h * 0.275))) 

        #screen.blit(Add_Record_Txt, Add_Record_Txt.get_rect(center = Add_Record.rect.center))

        click_ani.update()
        click_ani.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

#Choose character
def Choose_Character_Set(alpha, chr_set, race_len):
    change_menu = False
    update_bg = True
    fps = 0
    tru_fps = 0

    #Load Assets
    bg_List = ['Assets/background/ocean.png', 
                'Assets/background/forest/forest-1.png',
                'Assets/background/village/village.png',
                'Assets/background/Street/city.png',
                'Assets/test.jpg',
                'Assets/in_game_bg.png']

    
    title = Font(int(60 * size.w /1280)).render(Updt_Lang(lang, 'Select_Char', 'Char_Set'), True, "#D0312D")

    setA = Button('image', None, None, 'Assets/background/ocean.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/ocean.png', (size.w * 0.1, size.h * 0.35)) 
    setB = Button('image', None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/forest/forest-1.png', (size.w * 0.3, size.h * 0.35))
    setC = Button('image', None, None, 'Assets/background/village/village.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/village/village.png', (size.w * 0.5, size.h * 0.35))
    setD = Button('image', None, None, 'Assets/background/Street/city.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/Street/city.png', (size.w * 0.7, size.h * 0.35))
    setE = Button('image', None, None, 'Assets/test.jpg', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/test.jpg', (size.w * 0.9, size.h * 0.35))

    bounding_box = pg.rect.Rect((0,0), (size.w * 0.1505, size.h * 0.205))

    settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (50*size.w/1280, 50* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.975, size.h * 0.045))
    
    next = Button('image', None, None, 'Assets/icon/Settings/continue_01.png', (50*size.w/1280, 50* size.w/1280), None, None, None, None, 'Assets/icon/Settings/continue_02.png', (size.w*0.98, size.h * 0.955))

    back = Button('image', None, None, 'Assets/icon/Settings/return_01.png', (50*size.w/1280, 50* size.w/1280), None, None, None, None, 'Assets/icon/Settings/return_02.png', (size.w*0.02, size.h * 0.955)) 

    while True:
        alpha += 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Go to Settings Page
                if change_menu == False:
                    if settings.Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Menu('Choose_Character_Set', chr_set, race_len)
                    
                    #Change character set when user click on it
                    if next.Click(mouse_pos) and chr_set != 5:
                        Choose_Race_Length(-20, chr_set, race_len)

                    if setA.Click(mouse_pos):
                        chr_set = 0
                        update_bg = True

                    if setB.Click(mouse_pos):
                        chr_set = 1
                        update_bg = True

                    if setC.Click(mouse_pos):
                        chr_set = 2
                        update_bg = True

                    if setD.Click(mouse_pos):
                        chr_set = 3
                        update_bg = True

                    if setE.Click(mouse_pos):
                        chr_set = 4
                        update_bg = True

                    #Return to In_Game_Menu with alpha of -20 for fade in animations
                    if back.Click(mouse_pos):
                        In_Game_Menu(255)
            
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        if update_bg:
            background = pg.transform.scale(pg.image.load(bg_List[chr_set]).convert_alpha(), (512, 288))
            background = pg.transform.smoothscale(background, (size.w*1.075, size.h*1.075))
        
        match chr_set:
            case 0:
                bounding_box.center = setA.rect.center
            case 1:
                bounding_box.center = setB.rect.center
            case 2:
                bounding_box.center = setC.rect.center
            case 3:
                bounding_box.center = setD.rect.center
            case 4:
                bounding_box.center = setE.rect.center
            
        update_bg = False
        
        screen.fill(0)

        #Background moves with cursor
        Bg = Bg_Ani(background, (size.w / 2, size.h / 2), mouse_pos)
        Bg.Draw()

        #Temporary: Show what you have selected
        selected = Font(40).render(f'{Updt_Lang(lang, 'Select_Char', f'{chr_set}')}', True, '#ffffff')

        #Fade in animations
        for item in [background, back.image, next.image, settings.image, 
                    setA.image, setB.image, setC.image, setD.image, setE.image, selected]:
            item.set_alpha(alpha)
        
        #Blit assets onto screen
        for item in [settings, back, next, setA, setB, setC, setD, setE]:
            item.Blit(0,10)
            if alpha > 225 and change_menu == False:
                item.Hover(mouse_pos,0,10)   

        screen.blit(title, title.get_rect(center = (size.w * 0.5, size.h * 0.15)))
        screen.blit(selected, selected.get_rect(center = (size.w/2, size.h * 0.55)))

        if chr_set != 5:
            pg.draw.rect(screen, "#FFFFFF", bounding_box, 5, 0)
            
        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        click_ani.update()
        click_ani.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

#Choose race length
def Choose_Race_Length(alpha, chr_set, race_len):
    change_menu = False
    fps = 0
    tru_fps = 0
    bg_List = ['Assets/background/ocean.png', 
                'Assets/background/forest/forest-1.png',
                'Assets/background/village/village.png',
                'Assets/background/Street/city.png',
                'Assets/test.jpg',
                'Assets/in_game_bg.png']

    #Load Assets
    background = pg.transform.scale(pg.image.load(bg_List[chr_set]).convert_alpha(), (512, 288))
    background = pg.transform.smoothscale(background, (size.w*1.075, size.h*1.075))

    prompt = Font(int(60 * size.w /1280)).render(Updt_Lang(lang, 'Race_Len', 'Len'), True, "#FFFFFF")
    bounding_box = pg.rect.Rect((0,0), (size.w * 0.1505, size.h * 0.205))

    lengthA = Button('image', None, None, 'Assets/background/length/lap01.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/length/lap01.png', (size.w * 0.25, size.h * 0.35)) 
    lengthB = Button('image', None, None, 'Assets/background/length/lap02.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/length/lap02.png', (size.w * 0.5, size.h * 0.35))
    lengthC = Button('image', None, None, 'Assets/background/length/lap03.png', (size.w * 0.15, size.h * 0.2), None, None, None, None, 'Assets/background/length/lap03.png', (size.w * 0.75, size.h * 0.35))
    
    settings = Button('image', None, None, 'Assets/icon/Settings/setting_01.png', (50*size.w/1280, 50* size.w/1280), 
                    None, None, None, None, 'Assets/icon/Settings/setting_02.png', (size.w * 0.975, size.h * 0.045))
    
    enter = Button('image', None, None, 'Assets/icon/Settings/continue_01.png', (50*size.w/1280, 50* size.w/1280), None, None, None, None, 'Assets/icon/Settings/continue_02.png', (size.w*0.98, size.h * 0.955))


    back = Button('image', None, None, 'Assets/icon/Settings/return_01.png', (50*size.w/1280, 50* size.w/1280), None, None, None, None, 'Assets/icon/Settings/return_02.png', (size.w*0.02, size.h * 0.955)) 


    while True:
        alpha += 7.5
        fps += 1
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))


                if change_menu == False:

                    #Go to Settings Page
                    if settings.Click(mouse_pos):
                        pg.image.save(screen, 'Assets/temps/temp.png')
                        Video_Menu('Choose_Race_Length', chr_set, race_len)

                    #Change character set when user click on it
                    if lengthA.Click(mouse_pos):
                        race_len = 0

                    if lengthB.Click(mouse_pos):
                        race_len = 1

                    if lengthC.Click(mouse_pos):
                        race_len = 2

                    
                    #Debug: if user click start then print out what user has choosen 
                    if enter.Click(mouse_pos) and race_len != 3 :
                        current_user.Update_Coin(-200)
                        print(f'Selected: {chr_set}')
                        print(f'Selected: {race_len}')
                        Core_Game(chr_set, race_len)
                        
                    #Return to Choose_Character screen and preserve what the user chose
                    if back.Click(mouse_pos):
                        Choose_Character_Set(-20, chr_set, race_len)
            
            if event.type == Bg_cycle:
                tru_fps = fps
                fps = 0

        match race_len:
            case 0:
                bounding_box.center = lengthA.rect.center
            case 1:
                bounding_box.center = lengthB.rect.center
            case 2:
                bounding_box.center = lengthC.rect.center
        

        screen.fill(0)

        #Background moves with cursor
        bg = Bg_Ani(background, (size.w / 2, size.h / 2), mouse_pos)

        #Temporary:
        selected = Font(40).render(f'{Updt_Lang(lang, 'Race_Len', f'{race_len}')}', True, '#ffffff')

        #Fade in animation
        for item in [background, back.image, enter.image, settings.image, lengthA.image, lengthB.image, lengthC.image, selected]:
            item.set_alpha(alpha)

        
        bg.Draw()
        screen.blit(prompt, prompt.get_rect(center = (size.w /2, size.h * 0.125)))
        screen.blit(selected, selected.get_rect(center = (size.w/2, size.h * 0.55)))
        

        #Blit assets onto the screen
        for item in [settings, back, enter, lengthA, lengthB, lengthC]:
            item.Blit(0,10)
        
        #Change colors if the mouse hover above and only when alpha is high enough (finished fade in animation)
        if alpha > 225 and change_menu == False:
            for button in [settings, enter, back, lengthA, lengthB, lengthC]:
                button.Hover(mouse_pos, 0 ,10)
        

        if race_len != 3:
            pg.draw.rect(screen, "#FFFFFF", bounding_box, 5, 0)

        FPS = Font(int(30 * size.w / 1280)).render(f"FPS: {tru_fps}", True, "Black")
        screen.blit(FPS, (0,0))
    
        click_ani.update()
        click_ani.draw(screen)

        pg.time.Clock().tick(60)
        pg.display.update()

def Core_Game(theme, length):
    theme_list = ['ocean', 'forest', 'villager', 'street']
    baseSize = 90
    baseSpeed = 2

    bg = pg.image.load(f'Assets/background/{theme_list[theme]}.png').convert()
    bg = pg.transform.scale(bg, (1280,720))

    fps = pg.time.Clock()

    class Char:
        def __init__(self, x, y, speed, image_path):
            self.x = x
            self.y = y
            self.speed = speed
            self.act_i = 0
            self.status = 'idle'
            self.laps = 0
            self.orientation = 1
            # Tải hình ảnh từ đường dẫn được cung cấp
            self.walk = [pg.image.load(image_path + f'/walk_1.png'),
                        pg.image.load(image_path + f'/walk_2.png'),
                        pg.image.load(image_path + f'/walk_3.png'),
                        pg.image.load(image_path + f'/walk_4.png')]
            
            self.stun = [pg.image.load(image_path + f'/death_1.png'),
                        pg.image.load(image_path + f'/death_2.png'),
                        pg.image.load(image_path + f'/death_3.png'),
                        pg.image.load(image_path + f'/death_4.png')]
            
            self.idle = [pg.image.load(image_path + f'/idle_1.png'),
                        pg.image.load(image_path + f'/idle_2.png'),
                        pg.image.load(image_path + f'/idle_3.png')]
            
            for i in range(4):
                self.walk[i]= pg.transform.scale(self.walk[i], (baseSize * size.w / 1280, baseSize * size.h / 720))
                self.stun[i]= pg.transform.scale(self.stun[i], (baseSize * size.w / 1280, baseSize * size.h / 720))

                if (i < 3):
                    self.idle[i]= pg.transform.scale(self.idle[i], (baseSize * size.w / 1280, baseSize * size.h / 720))

    #        self.image = pg.transform.scale(self.image, (50, 50))  # Thu nhỏ kích thước hình ảnh
            self.reverse = False
            self.teleport = False
            self.slow = False
            self.speedup = False
            self.finished = False
            self.effect_end_time = None
            self.wait_until = None  # Thời gian mà xe phải đợi trước khi di chuyển tiếp

        def draw(self,act_i,status):
            if status == 'walk':
                if self.orientation == 1:
                    screen.blit(self.walk[act_i//15], (self.x, self.y)) # Vẽ hình ảnh
                elif self.orientation == -1:
                    screen.blit(pg.transform.flip(self.walk[act_i//15],1,0), (self.x, self.y))

            elif status == 'stun':
                if self.orientation == 1:
                    screen.blit(self.stun[act_i//15], (self.x, self.y)) # Vẽ hình ảnh
                elif self.orientation == -1:
                    screen.blit(pg.transform.flip(self.stun[act_i//15],1,0), (self.x, self.y))

            else:
                if self.orientation == 1:
                    screen.blit(self.idle[act_i//15], (self.x, self.y)) # Vẽ hình ảnh
                elif self.orientation == -1:
                    screen.blit(pg.transform.flip(self.idle[act_i//15],1,0), (self.x, self.y))

            if status == 'idle':
                if act_i == 44:
                    return 0
                else:
                    return act_i + 1
                
            else:
                if act_i == 59:
                    if status == 'stun':
                        return act_i
                    else:   
                        return 0
                    
                else:
                    return act_i + 1  # Vẽ hình ảnh thay vì hình vuông
            
        def move(self):
            if self.wait_until and pg.time.get_ticks() < self.wait_until:
                self.status = 'stun'
                return  # Nếu xe đang trong thời gian chờ, không di chuyển nó
            
            if not self.finished:
                self.status = 'walk'

            if self.reverse:
                self.x -= self.speed

            elif self.slow:
                self.x += self.speed / 2

            elif self.speedup:
                self.x += self.speed * 2.5

            else:
                self.x += self.speed

            if self.effect_end_time and pg.time.get_ticks() > self.effect_end_time:
                self.reverse = False
                self.slow = False
                self.speedup = False
                self.effect_end_time = None
        
        def is_clicked(self, pos):
            return self.x <= pos[0] <= self.x + baseSize * size.w / 1280 and self.y <= pos[1] <= self.y + baseSize * size.h / 720

        def collides_with(self, obstacle):
            return self.x < obstacle.x + baseSize * size.w / 1280 and self.x + baseSize * size.w / 1280 > obstacle.x and self.y < obstacle.y + baseSize * size.h / 720 and self.y + baseSize * size.h / 720 > obstacle.y

    # Tạo danh sách các xe với hình ảnh tương ứng
    chars = [Char(50, 30 + (i + 1)*0.15*size.h, uniform(baseSpeed * 1,baseSpeed * 2) * size.w / 1280, f'Assets/char/animation/{theme_list[theme]}/{theme_list[theme]}_{i+1}') for i in range(5)]

    class Obstacle:
        def __init__(self, x, y, image_paths):
            self.x = x
            self.y = y
            self.image_paths = image_paths
            self.set_image('Assets/Obstacles/obstacle_box.png')
            self.changed = False  # Thêm thuộc tính này để theo dõi xem hình ảnh đã được thay đổi chưa
            self.change_time = None  # Thêm thuộc tính này để theo dõi thời gian mà hình ảnh đã được thay đổi

        def set_image(self, image_path):
            self.image = pg.image.load(image_path)  # Tải hình ảnh từ đường dẫn được cung cấp
            self.image = pg.transform.scale(self.image, (baseSize * size.w / 1280, baseSize * size.h / 720))  # Thu nhỏ kích thước hình ảnh

        def set_random_image(self):
            if not self.changed:
                self.image_path = choice(self.image_paths)  # Lưu trữ hình ảnh hiện tại
                self.set_image(self.image_path)
                self.changed = True
                self.change_time = pg.time.get_ticks()
                return self.image_path  # Trả về hình ảnh đã chọn

        def draw(self):
            screen.blit(self.image, (self.x, self.y))# Vẽ hình ảnh   
    # Tạo danh sách các chướng ngại vật ở nửa đường
    obstacle_images = ['Assets/Obstacles/obstacle_confinement.png', 'Assets/Obstacles/obstacle_finish.png', 
                    'Assets/Obstacles/obstacle_reverse.png', 'Assets/Obstacles/obstacle_slow.png', 
                    'Assets/Obstacles/obstacle_speed.png', 'Assets/Obstacles/obstacle_teleport.png', 
                    'Assets/Obstacles/obstacle_tostart.png']
    obstacles = [Obstacle(uniform(size.w*0.3, size.w*0.7), 30 + 0.15*size.h*(i+1), obstacle_images) for i in range(5)]
    # Hàm hiển thị menu và nhận lựa chọn từ người chơi
    def show_menu():
        running = True
        selection = 0
        charImage = Draw_to_Screen('text', None, None, None, None, '', 
                                        Font(int(50 * size.w / 1280)), '#FFFFFF', (size.w * 0.60, size.h * 0.5))
        while running:
            screen.blit(bg,(0,0))

            text = Draw_to_Screen('text', None, None, None, None, 'Choose your character!', 
                        Font(int(70 * size.w / 1280)), '#FFFFFF', (size.w * 0.5, size.h * 0.3))
            
            currentChar = Draw_to_Screen('text', None, None, None, None, 'Your character:', 
                        Font(int(50 * size.w / 1280)), '#FFFFFF', (size.w * 0.4, size.h * 0.5))
            
            Start = Button('rect', (size.w*0.4, size.h * 0.65), (size.w*0.175, size.h * 0.075), None, None, None, None, '#FFFFFF', '#FFFFFF' , None, None)
            Start_text = Draw_to_Screen('text', None, None, None, None, 'Start', Font((40)), '#000000', Start.rect.center)
            
            for item in [text, currentChar, charImage, Start, Start_text]:
                item.Blit(0,0)

            fps.tick(60)
            for char in chars:
                char.act_i = char.draw(char.act_i,char.status)

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Shutdown()  
                    # Thoát khỏi chương trình nếu người dùng đóng cửa sổ

                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()

                    for i, char in enumerate(chars):
                        if char.is_clicked(pos):
                            charImage = Draw_to_Screen('image', None, None, f'Assets/char/animation/{theme_list[theme]}/{theme_list[theme]}_{i+1}/idle_1.png', ((baseSize * 1.2)*size.w/1280, (baseSize * 1.2)* size.w/1280), None, 
                                        None, None, (size.w * 0.6, size.h * 0.5))
                            selection = i                # Trả về chỉ số của xe mà người dùng đã chọn
                        if Start.Click(pos):
                            return selection
                            
                    

    # Hỏi người chơi chọn xe
    player_choice = show_menu()

    # Tạo một danh sách để theo dõi thứ tự các xe về đích
    finish_order = []
    ranking_list = [0, 0, 0, 0, 0]

    # Vòng lặp chính của game
    running = True
    for char in chars:
        char.status = 'walk'
        
    Finish = Button('rect', (size.w*0.4, size.h * 0.65), (size.w*0.175, size.h * 0.075), None, None, None, None, '#FFFFFF', '#FFFFFF' , None, None)
    Finish_text = Draw_to_Screen('text', None, None, None, None, 'Next', Font((40)), '#000000', Finish.rect.center)

    all_Finish = False

    while running:
        # Xử lý các sự kiện
            fps.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if (event.type == pg.MOUSEBUTTONDOWN):
                    mouse_pos = pg.mouse.get_pos()
                    if all_Finish:
                        if Finish.Click(mouse_pos):
                            running = False
                            Result_Screen.Show_Result(ranking_list, player_choice, theme, screen)
                            In_Game_Menu(-20)

            screen.blit(bg,(0,0))
            
            if all_Finish:
                Finish.Blit(0,0)
                Finish_text.Blit(0,0)
            
            # Vẽ và di chuyển các xe
            for char in chars:
                char.act_i = char.draw(char.act_i, char.status)
                char.move()
                image_path = None  # Khởi tạo image_path với giá trị mặc định
                for obstacle in obstacles:
                    if char.collides_with(obstacle):
                        image_path = obstacle.set_random_image()  # Lấy hình ảnh đã chọn
                if image_path:  # Kiểm tra nếu image_path không phải là None
            
                    if 'obstacle_confinement.png' in image_path:  # Kiểm tra hình ảnh hiện tại của chướng ngại vật
                        char.wait_until = pg.time.get_ticks() + 1000 # Đặt thời gian chờ cho xe
                        char.status = 'stun'
                    elif 'obstacle_finish.png' in image_path:
                        if (char.speed > 0):
                            char.x = 0.95 * size.w
                        else:
                            char.x = 0.05 * size.w
                    elif 'obstacle_reverse.png' in image_path:
                        char.reverse = True
                        char.effect_end_time = pg.time.get_ticks() + 1000
                    elif 'obstacle_slow.png' in image_path:
                        char.slow = True
                        char.effect_end_time = pg.time.get_ticks() + 1000
                    elif 'obstacle_speed.png' in image_path:
                        char.speedup = True
                        char.effect_end_time = pg.time.get_ticks() + 500
                    elif 'obstacle_teleport.png' in image_path:
                        char.x += char.speed/(abs(char.speed)) * 200 * size.w / 1280
                    elif 'obstacle_tostart.png' in image_path:
                        if (char.speed > 0):
                            char.x = 0.05 * size.w
                        else:
                            char.x = 0.95 * size.w
                                        
            # Vẽ chướng ngại vật
            for obstacle in obstacles:
                obstacle.draw()

            # Loại bỏ các chướng ngại vật đã thay đổi hình ảnh từ hơn 2 giây trước
            obstacles = [obstacle for obstacle in obstacles if not obstacle.changed or pg.time.get_ticks() - obstacle.change_time < 2000]

            # Cập nhật màn hình
            pg.display.flip()

            # Kiểm tra xem có xe nào về đích chưa
            for i, char in enumerate(chars):
                if (char.x >= 0.95*size.w and char.laps % 2 == 0) or (char.x <= 0.05*size.w and char.laps % 2 == 1):
                    if char.laps == length and i not in finish_order:
                        finish_order.append(i)
                        if len(finish_order) == 1:
                            ranking_list[2] = i + 1
                        elif len(finish_order) == 2:
                            ranking_list[3] = i + 1
                        elif len(finish_order) == 3:
                            ranking_list[1] = i + 1
                        elif len(finish_order) == 4:
                            ranking_list[0] = i + 1
                        elif len(finish_order) == 5:
                            ranking_list[4] = i + 1
                        print(ranking_list)
                        char.speed = 0
                        if length % 2 == 0:
                            char.x = size.w*0.95
                        else:
                            char.x = size.w*0.05
                        char.status = 'idle'
                        char.act_i = 0
                        char.finished = True
                        print(f"Xe số {i+1} đã về đích!")
                        print(char.laps)
                    elif not char.finished:
                        obstacles.append(Obstacle(uniform(size.w*0.3, size.w*0.7), 30 + 0.15*size.h*(i+1), obstacle_images))
                        char.laps += 1
                        char.speed = -1*char.speed
                        char.orientation = -char.orientation

            
            # Nếu tất cả các xe đều đã về đích, kết thúc trò chơi và công bố kết quả
            if len(finish_order) == len(chars):
                all_Finish = True
    #            print("Tất cả các xe đã về đích!")
    #            for i, char_index in enumerate(finish_order):
    #                if i == 0 and char_index == player_choice:
    #                    player_gold += 20
    #                    result_text = f"Your car comes first! You have received 20 gold. Your current gold amount is {player_gold}."
    #                else:
    #                    result_text = f"Car number {char_index+1} came in {i+1}th place."
    #        
    #                # Tạo font và vẽ văn bản lên màn hình
    #                font = pg.font.Font(None, 36)
    #                text = font.render(result_text, True, (255, 255, 255))
    #                screen.blit(text, (250 * size.w / 1280, (300 + i * 40) * size.h / 720))  # Thay đổi vị trí y để các dòng văn bản không chồng lên nhau

                # Cập nhật màn hình để hiển thị văn bản
                pg.display.flip()

                # Đợi một chút trước khi thoát để người chơi có thể đọc kết quả
                # pg.time.wait(5000)

#Settings Tab
def Video_Menu(prev_menu, set_char, race_len):
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
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Go to different setting menus
                if audio.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Menu(prev_menu, set_char, race_len)

                if language.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Menu(prev_menu, set_char, race_len)

                if user_center.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Menu(prev_menu, set_char, race_len)

                if back.Click(mouse_pos) and prev_menu != 'Title':
                    Title(True)

                #If return is pressed, return to a previous menu
                if close.Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Title':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_len)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_len)
                
                #Change resolutions
                if Full_Screen.Click(mouse_pos):
                    sfx_channels.play(interface)
                    in_full_screen = True
                    size.Full_Screen()

                if _1366x768.Click(mouse_pos):
                    sfx_channels.play(interface)
                    in_full_screen = False
                    size.Window((1366, 768))

                if _1280x720.Click(mouse_pos):
                    sfx_channels.play(interface)
                    in_full_screen = False
                    size.Window((1280, 720))    

            #Update everything within the menu when size changed
            if event.type == pg.WINDOWSIZECHANGED:
                change_size = True

        #If a size change is detected, create new object that replace the old one with new resolution
        if change_size:

            bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))
            menu_box = pg.rect.Rect(size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75)

            video = Draw_to_Screen('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
            audio = Button('rect', video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            language = Button('rect', audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            user_center = Button('rect', language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            back = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
            close = Button('image', None, None, 'Assets/icon/Settings/close.png', (40*size.w/1280, 40*size.w/1280), None, None, None, None , 'Assets/icon/Settings/close-1.png', (0,0))
            close.rect.center = menu_box.topright

            Full_Screen = Button('rect', (size.w * 0.325, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            _1366x768 = Button('rect', (size.w * 0.5125, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            _1280x720 = Button('rect', (size.w * 0.7, size.h * 0.2), (size.w*0.15, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
            
            video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
            audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
            language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
            user_center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
            back_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')
            

            Full_Screen_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Video', 'Full_Screen' ), True, '#424769')
            _1366x768_text = Font(int(25 * size.w / 1280)).render('1366 x 768', True, '#424769')
            _1280x720_text = Font(int(25 * size.w / 1280)).render('1280 x 720', True, '#424769')
            
            

        #After all the object has been updated, change the variable to False
        change_size = False

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', menu_box)
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [video, audio, language, user_center, close]:
            item.Blit(0,0)
        
        for item in [Full_Screen, _1366x768, _1280x720]:
            item.Blit(0,10)

        #Change colors if the mouse hover above
        for button in [audio, language, user_center]:
            button.Hover(mouse_pos, 0 , 0)

        for button in [Full_Screen, _1366x768, _1280x720, close]:
            button.Hover(mouse_pos, 0 , 10)
        
        if prev_menu != 'Title':
            back.Blit(0,0)
            back.Hover(mouse_pos, 0, 0)
            screen.blit(back_text, back_text.get_rect(center = (back.rect.center)))
            


        #Blit Settings Text onto screen
        screen.blit(video_text, video_text.get_rect(center = (video.rect.center)))
        screen.blit(audio_text, audio_text.get_rect(center = (audio.rect.center)))
        screen.blit(language_text, language_text.get_rect(center = (language.rect.center)))
        screen.blit(user_center_text, user_center_text.get_rect(center = (user_center.rect.center)))
        

        #Blit Video Texts onto screen
        screen.blit(Full_Screen_text, Full_Screen_text.get_rect(center = (Full_Screen.rect.center)))
        screen.blit(_1366x768_text, _1366x768_text.get_rect(center = (_1366x768.rect.center)))
        screen.blit(_1280x720_text, _1280x720_text.get_rect(center = (_1280x720.rect.center)))

        #Mouse Animation
        click_ani.update()
        click_ani.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Audio_Menu(prev_menu, set_char, race_len):
    global music_volume, sfx_volume
    
    #Load Assets
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = bg = pg.transform.smoothscale(bg, (size.w, size.h))
    menu_box = pg.rect.Rect(size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75)

    video = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    audio = Draw_to_Screen('rect', video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    language = Button('rect', audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    user_center = Button('rect', language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    back = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    close = Button('image', None, None, 'Assets/icon/Settings/close.png', (40*size.w/1280, 40*size.w/1280), None, None, None, None , 'Assets/icon/Settings/close-1.png', (0,0))
    close.rect.center = menu_box.topright

    music_slider = pg.rect.Rect((0, 0), (300 * size.w/1280, 20 * size.h/720))
    music_slider.center = (size.w * 0.7, size.h * 0.25)

    music_circle = pg.rect.Rect((0,0), (30 * size.w/1280, 30 * size.w/1280))
    music_circle.center = (music_volume * (music_slider.right - music_slider.left) + music_slider.left, size.h * 0.25)

    sfx_slider = pg.rect.Rect((0, 0), (300 * size.w/1280, 20 * size.h/720))
    sfx_slider.center = (size.w * 0.7, size.h * 0.4)

    sfx_circle = pg.rect.Rect((0,0), (30 * size.w/1280, 30 * size.w/1280))
    sfx_circle.center = (sfx_volume * (sfx_slider.right - sfx_slider.left) + sfx_slider.left, size.h * 0.4)

    video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
    audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
    language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
    user_center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
    back_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')

    music_text = Font(int(25*size.w/1280)).render(Updt_Lang(lang, 'Audio', 'Music' ), True, '#FFFFFF')
    sfx_text = Font(int(25*size.w/1280)).render(Updt_Lang(lang, 'Audio', 'SFX' ), True, '#FFFFFF')

    while True:

        #Position of the mouse
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Go to different setting menus
                if video.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Menu(prev_menu, set_char, race_len)

                if language.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Menu(prev_menu, set_char, race_len)

                if user_center.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Menu(prev_menu, set_char, race_len)
                    
                if back.Click(mouse_pos) and prev_menu != 'Title':
                    Title(True)

                #If return is pressed, return to a previous menu
                if close.Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Title':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_len)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_len)


        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', menu_box)
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
        for item in [video, audio, language, user_center, close]:
            item.Blit(0,0)

        #Change colors if the mouse hover above
        for button in [video, language, user_center, close]:
            button.Hover(mouse_pos, 0 ,0)
        
        #Blit Settings Text onto screen
        screen.blit(video_text, video_text.get_rect(center = (video.rect.center)))
        screen.blit(audio_text, audio_text.get_rect(center = (audio.rect.center)))
        screen.blit(language_text, language_text.get_rect(center = (language.rect.center)))
        screen.blit(user_center_text, user_center_text.get_rect(center = (user_center.rect.center)))

        screen.blit(music_text, music_text.get_rect(midleft = (size.w * 0.35, size.h * 0.25)))
        screen.blit(sfx_text, sfx_text.get_rect(midleft = (size.w * 0.35, size.h * 0.4)))

        if prev_menu != 'Title':
            back.Blit(0,0)
            back.Hover(mouse_pos, 0, 0)
            screen.blit(back_text, back_text.get_rect(center = (back.rect.center)))

        #Mouse animation
        click_ani.update()
        click_ani.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def Language_Menu(prev_menu, set_char, race_len):
    global lang
    change_language = True

    #Load Assets
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))
    menu_box = pg.rect.Rect(size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75)

    video = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    audio = Button('rect', video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d','#5d648c', None, None)
    language = Draw_to_Screen('rect', audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    user_center = Button('rect', language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    back= Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    close = Button('image', None, None, 'Assets/icon/Settings/close.png', (40*size.w/1280, 40*size.w/1280), None, None, None, None , 'Assets/icon/Settings/close-1.png', (0,0))
    close.rect.center = menu_box.topright

    choose_US = Button('rect', (size.w*0.375, size.h * 0.2), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    choose_VN = Button('rect', (size.w*0.625, size.h * 0.2), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)

    choose_US_text = Font(int(25 * size.w / 1280)).render('English', True, '#424769')
    choose_VN_text = Font(int(25 * size.w / 1280)).render('Tiếng Việt', True, '#424769')

    while True:

        #Position of the mouse
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Change global langauge settings
                if choose_US.Click(mouse_pos) == True:
                    sfx_channels.play(interface)
                    change_language = True
                    lang = 'US'

                if choose_VN.Click(mouse_pos) == True:
                    sfx_channels.play(interface)
                    change_language = True
                    lang = 'VN'

                #Go to different setting menus
                if video.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Menu(prev_menu, set_char, race_len)

                if audio.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Menu(prev_menu, set_char, race_len)

                if user_center.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    User_Center_Menu(prev_menu, set_char, race_len)
                
                if back.Click(mouse_pos) and prev_menu != 'Title':
                    Title(True)

                #If return is pressed, return to a previous menu
                if close.Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Title':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_len)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_len)

        #Update global lang
        if change_language == True:
            video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
            audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
            language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
            user_center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
            back_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')

        #After update, return variable to False
        change_language = False

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', menu_box)
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [choose_US, choose_VN]:
            item.Blit(0,10)
        
        for item in [video, audio, language, user_center, close]:
            item.Blit(0,0)

        #Change colors if the mouse hover above
        for button in [choose_US, choose_VN]:
            button.Hover(mouse_pos, 0 ,10)

        for button in [video, audio, user_center, close]:
            button.Hover(mouse_pos, 0 ,0)
        
        #Blit settings text onto the screen
        screen.blit(video_text, video_text.get_rect(center = (video.rect.center)))
        screen.blit(audio_text, audio_text.get_rect(center = (audio.rect.center)))
        screen.blit(language_text, language_text.get_rect(center = (language.rect.center)))
        screen.blit(user_center_text, user_center_text.get_rect(center = (user_center.rect.center)))

        screen.blit(choose_US_text, choose_US_text.get_rect(center = (choose_US.rect.center)))
        screen.blit(choose_VN_text, choose_VN_text.get_rect(center = (choose_VN.rect.center)))

        if prev_menu != 'Title':
            back.Blit(0,0)
            back.Hover(mouse_pos, 0, 0)
            screen.blit(back_text, back_text.get_rect(center = (back.rect.center)))


        
        click_ani.update()
        click_ani.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

def User_Center_Menu(prev_menu, set_char, race_len):

    #Load Assets
    bg = pg.transform.smoothscale(pg.image.load('Assets/temps/temp.png').convert(), (512,288))
    bg = pg.transform.smoothscale(bg, (size.w, size.h))
    menu_box = pg.rect.Rect(size.w*0.125, size.h * 0.125, size.w*0.75, size.h * 0.75)

    video = Button('rect', (size.w*0.125, size.h * 0.125), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    audio = Button('rect', video.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    language = Button('rect', audio.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    user_center = Draw_to_Screen('rect', language.rect.bottomleft, (size.w*0.175, size.h * 0.1), None, None, None, None, '#f9b17a', None)
    back = Button('rect', (size.w*0.125, size.h*0.775), (size.w*0.175, size.h * 0.1), None, None, None, None, '#676f9d', '#5d648c', None, None)
    close = Button('image', None, None, 'Assets/icon/Settings/close.png', (40*size.w/1280, 40*size.w/1280), None, None, None, None , 'Assets/icon/Settings/close-1.png', (0,0))
    close.rect.center = menu_box.topright

    change_username = Button('rect', (size.w * 0.425, size.h * 0.2), (size.w*0.3, size.h * 0.1), None, None, None, None, '#676f9d', '#f9b17a', None, None)
    
    video_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Video' ), True, '#424769')
    audio_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Audio' ), True, '#424769')
    language_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Language' ), True, '#424769')
    user_center_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'User_Center' ), True, '#424769')
    back_text = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'Settings', 'Return' ), True, '#424769')
    change_username_txt = Font(int(25 * size.w / 1280)).render(Updt_Lang(lang, 'User_Center', 'Change_Username' ), True, '#424769')

    while True:

        #Get mouse position
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Shutdown()

            if event.type == pg.MOUSEBUTTONDOWN:
                click_ani.add(Click_Ani(mouse_pos, 5, size.w))

                #Go to different setting menus
                if video.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Video_Menu(prev_menu, set_char, race_len)

                if audio.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Audio_Menu(prev_menu, set_char, race_len)

                if language.Click(mouse_pos):
                    sfx_channels.play(button_click)
                    Language_Menu(prev_menu, set_char, race_len)
                
                if back.Click(mouse_pos) and prev_menu != 'Title':
                    Title(True)
                
                if change_username.Click(mouse_pos):
                    Enter_Username('Settings', prev_menu, set_char, race_len)

                #If return is pressed, return to a previous menu
                if close.Click(mouse_pos):
                    sfx_channels.play(button_click)

                    if prev_menu == 'Title':
                        Title(False)

                    elif prev_menu == 'In_Game_Menu':
                        In_Game_Menu(0)

                    elif prev_menu == 'Choose_Character_Set':
                        Choose_Character_Set(-20, set_char, race_len)

                    elif prev_menu == 'Choose_Race_Length':
                        Choose_Race_Length(-20, set_char, race_len)

        screen.blit(bg, (0,0))
        pg.draw.rect(screen, '#2d3250', menu_box)
        pg.draw.rect(screen, '#676f9d', [size.w*0.125, size.h * 0.125, size.w*0.175, size.h * 0.75])

        #Blit Assets onto screen
        for item in [video, audio, language, user_center, close]:
            item.Blit(0,0)

        #Change colors if the mouse hover above
        for button in [video, audio, language, close]:
            button.Hover(mouse_pos, 0 ,0)

        change_username.Blit(0,10)
        change_username.Hover(mouse_pos,0,10)
        
        #Blit text onto the screen
        screen.blit(video_text, video_text.get_rect(center = (video.rect.center)))
        screen.blit(audio_text, audio_text.get_rect(center = (audio.rect.center)))
        screen.blit(language_text, language_text.get_rect(center = (language.rect.center)))
        screen.blit(user_center_text, user_center_text.get_rect(center = (user_center.rect.center)))
        screen.blit(change_username_txt, change_username_txt.get_rect(center = change_username.rect.center))

        if prev_menu != 'Title':
            back.Blit(0,0)
            back.Hover(mouse_pos, 0, 0)
            screen.blit(back_text, back_text.get_rect(center = (back.rect.center)))

        click_ani.update()
        click_ani.draw(screen)

        pg.display.update()
        pg.time.Clock().tick(60)

Load_Config()
Login('23120050@student.hcmus.edu.vn', '1234567890')
#Mini_Game_Menu()
