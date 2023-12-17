import pygame as pg
import json
import sqlite3
import os
import hashlib


try:
    with open ('settings/Config.json', 'r') as f:
        config = json.load(f)
        start_screen_size = config['Start_Screen_Size'][1:-1]
        start_screen_size = tuple(map(int, start_screen_size.split(', ')))
        in_full_screen = config['In_Full_Screen']
except:
    start_screen_size = (0,0)
    in_full_screen = 'True'


conn = sqlite3.connect('database/User_Data.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS User_Data(
            User_ID INTEGER PRIMARY KEY,
            Email VAR CHAR(255) NOT NULL,
            Password VAR CHAR(255) NOT NULL,
            Username VAR CHAR (255),
            Coins VAR CHAR (255) NOT NULL)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS User_History(
            History_ID INTEGER PRIMARY KEY,
            User_ID INTEGER,
            Selected_Char VAR CHAR(255),
            Race_Length VAR CHAR(255),
            Result VAR CHAR(255),
            Coins_Change VAR CHAR (255),
            FOREIGN KEY(USER_ID) REFERENCES User_Data(User_ID)
)
""") 


global US, VN

#open config files
with open('locale/en_US.json', 'r', encoding = "utf8") as f:
    US = json.load(f)

with open('locale/vi_VN.json', 'r', encoding = "utf8") as f:
    VN = json.load(f)

def Font(size):
    return pg.font.Font('font/arial.ttf', size)


def Updt_Lang(lang, menu, name):


    if (lang == 'US')   :  return(f'{US[menu][name]}')
    elif (lang == 'VN') :  return(f'{VN[menu][name]}')

class Screen_Info:
    def __init__(self, current_size):
        self.w, self.h = current_size

    def Full_Screen(self):
        pg.display.set_mode((0,0), pg.SRCALPHA|pg.FULLSCREEN | pg.NOFRAME)
        self.w, self.h = screen.get_size()

    def Window(self, current_size):
        self.w, self.h = current_size
        pg.display.set_mode((self.w, self.h), pg.SRCALPHA| pg.NOFRAME)

class Click_Ani(pg.sprite.Sprite):
    def __init__(self, instant_mouse_pos, r, size) -> None:
        super().__init__()
        self.r = r
        self.size = size
        self.transparency = 255
        self.pos = instant_mouse_pos
        self.image = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/mouse_animation.png').convert_alpha(), 0, 0.005 * self.r)
        self.rect = self.image.get_rect(center = (self.pos))
    
    def Kill(self):
        if self.r >= 75 * self.size/1280:
            self.kill()
        
    def update(self):
        self.r += 1.5 * self.size/1280
        self.transparency -= 255 * (1.75 / 70)
        self.image = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/mouse_animation.png').convert_alpha(), 0, 0.004 * self.r)
        self.image.set_alpha(self.transparency)
        self.rect = self.image.get_rect(center = (self.pos))
        self.Kill()

class Bg_Ani():
    def __init__(self, bg, pos, mouse_pos):
        self.image = bg
        self.x, self.y = pos
        self.mouse_x, self.mouse_y = mouse_pos
        self.rect = self.image.get_rect(center = (self.x,  self.y))

    def Draw(self):
        self.rect = self.image.get_rect(center = (self.x + 0.03 * self.mouse_x, self.y + 0.035 * self.mouse_y))
        screen.blit(self.image, self.rect)

class Draw_to_Screen():
    def __init__(self, type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, pos):
        self.type = type
        self.pos = pos

        if self.type == 'image':
            self.x, self.y = pos
            self.image_file = image_file
            self.image_scale = image_scaling
            self.image = pg.transform.scale(pg.image.load(self.image_file).convert_alpha(), (self.image_scale))
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

    
    def Blit(self, width, radius):
        if self.type == 'image':
            screen.blit(self.image, self.rect)

        if self.type == 'text':
            screen.blit(self.text, self.rect)
        
        if self.type == 'rect':
            pg.draw.rect(screen, self.color, self.rect, width, radius)
      
class Button(Draw_to_Screen):
    def __init__(self, type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, alter_color, alter_image_file, pos):
        super().__init__(type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, pos)
        if type == 'rect' or type == 'text':
            self.alter_color = alter_color
        elif type == 'image':
            self.alter_image_file = alter_image_file
            self.alter_image = pg.transform.scale(pg.image.load(self.alter_image_file).convert_alpha(), (self.image_scale))
        

    def Hover(self, mouse_pos, width, radius):
        if self.rect.collidepoint(mouse_pos):
            if self.type == 'rect':
                pg.draw.rect(screen, self.alter_color, self.rect, width, radius)

            if self.type == 'text':
                self.text = self.font.render(self.text_content, True, self.alter_color)
                screen.blit(self.text, self.rect)

            if self.type == 'image':
                screen.blit(self.alter_image, self.rect)
        else:
            if self.type == 'text':
                self.text = self.font.render(self.text_content, True, self.color)
                screen.blit(self.text, self.rect)

    
    def Click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):  
            return True
        return False
    
    def Update(self, text_content, color, alter_color):
        if self.type == 'text':
            self.text_content = text_content
            self.color = color
            self.alter_color = alter_color
            self.text = self.font.render(self.text_content, True, self.color)

class User_Data:
    def __init__(self):
        self.email = None
        self.pwd = None
        self.username = None
        self.coin = None
        self.user_id = None

    def Login(self):
        cur.execute("SELECT * FROM User_Data WHERE Email = ? AND Password = ?", (self.email, self.pwd))
        if cur.fetchall():
            cur.execute("SELECT * FROM User_Data WHERE Email= ?", (self.email,))
            info = cur.fetchone()
            self.user_id = info[0]
            self.username = info[3]
            self.coin = int(info[4])
            
            return True
        else:
            return False

    def Sign_Up_Validate(self):
        cur.execute("SELECT * FROM User_Data WHERE Email = ?", (self.email,))
        if  cur.fetchall():
            return False
        else :
            return True
    
    def Sign_Up(self):
        cur.execute("INSERT INTO User_Data(Email, Password, Username, Coins) VALUES (?,?,?,?)", (self.email, self.pwd, self.username, 200))
        conn.commit()
        cur.execute("SELECT User_ID FROM User_DATA WHERE Email = ?", (self.email,))
        self.user_id = cur.fetchone()[0]
        self.coin = 200

    def Update_Username(self, username):
        self.username = username
        cur.execute("UPDATE User_Data SET Username = ? WHERE Email = ?", (self.username, self.email))
        conn.commit()

    def Update_Coin(self, change):
        self.coin += change
        cur.execute("""UPDATE User_Data
                    SET Coins = ?
                    WHERE Email = ?
                    """, (self.coin, self.email))
        conn.commit()
    
    def Save_History(self, chr_set, race_len, win, coin):
        cur.execute("""INSERT INTO User_History 
                    (User_ID,
                    Selected_Char, 
                    Race_Length, 
                    Result, 
                    Coins_Change)
                    VALUES (?,?,?,?,?)""",(self.user_id, chr_set, race_len, win, coin))
        conn.commit()

    def Get_History(self):
        cur.execute("SELECT * FROM User_History WHERE User_ID = ? ORDER BY History_ID DESC", (self.user_id,))
        return cur.fetchmany(6)

class Game_History():
    def __init__ (self, info, lang, size):
        self.info = info
        self.win = '#00FF00'
        self.lose = '#FF0000'

        if int(self.info[5]) > 0:
            self.chr_set = Font(int(30 * size/1280)).render(Updt_Lang(lang, 'History_Char', f'{self.info[2]}'), True, self.win)
            self.race_len = Font(int(30 * size/1280)).render(Updt_Lang(lang, 'History_Race', f'{self.info[3]}'), True, self.win)
            self.result = Font(int(30 * size/1280)).render(Updt_Lang(lang, 'History_Result', f'{self.info[4]}'), True, self.win)
            self.coins_change = Font(int(30 * size/1280)).render(f'{self.info[5]}', True, self.win)
            
        else:
            self.chr_set = Font(int(30 * size/1280)).render(Updt_Lang(lang, 'History_Char', f'{self.info[2]}'), True, self.lose)
            self.race_len = Font(int(30 * size/1280)).render(Updt_Lang(lang, 'History_Race', f'{self.info[3]}'), True, self.lose)
            self.result = Font(int(30 * size/1280)).render(Updt_Lang(lang, 'History_Result', f'{self.info[4]}'), True, self.lose)
            self.coins_change = Font(int(30 * size/1280)).render(f'{self.info[5]}', True, self.lose)

        self.chr_set_rect = self.chr_set.get_rect(center = (0,0))
        self.race_len_rect = self.race_len.get_rect(center = (0,0))
        self.result_rect = self.result.get_rect(center = (0,0))
        self.coins_change_rect = self.coins_change.get_rect(center = (0,0))
        
      
pg.init()
if in_full_screen == 'False':   
    screen = pg.display.set_mode(start_screen_size, pg.SRCALPHA | pg.NOFRAME)
elif in_full_screen == 'True':
    screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.SRCALPHA | pg.NOFRAME)
os.environ['SDL_VIDEO_CENTERED'] = '0'

