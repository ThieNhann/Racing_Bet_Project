import pygame as pg
import json
import sqlite3
import hashlib
from User_Database import *

with open ('settings/Config.json', 'r') as f:
    config = json.load(f)
    start_screen_size = config['Start_Screen_Size'][1:-1]
    start_screen_size = tuple(map(int, start_screen_size.split(', ')))
    in_full_screen = config['In_Full_Screen']
    print(in_full_screen)

class Screen_Info:
    def __init__(self, current_size):
        self.w, self.h = current_size

    def Full_Screen(self):
        pg.display.set_mode((0,0), pg.SRCALPHA|pg.FULLSCREEN)
        self.w, self.h = screen.get_size()

    def Window(self, current_size):
        self.w, self.h = current_size
        pg.display.set_mode((self.w, self.h))

class Mouse_Animation(pg.sprite.Sprite):
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

class Dynamic_Background():
    def __init__(self, bg, pos, mouse_pos):
        self.image = bg
        self.x, self.y = pos
        self.mouse_x, self.mouse_y = mouse_pos
        self.rect = self.image.get_rect(center = (self.x,  self.y))

    def Draw(self):
        self.rect = self.image.get_rect(center = (self.x + 0.03 * self.mouse_x, self.y + 0.035 * self.mouse_y))
        screen.blit(self.image, self.rect)

class Draw_Screen():
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
    
    def Blit(self):
        if self.type == 'image':
            screen.blit(self.image, self.rect)

        if self.type == 'text':
            screen.blit(self.text, self.rect)
        
        if self.type == 'rect':
            pg.draw.rect(screen, self.color, self.rect)
      
class Button(Draw_Screen):
    def __init__(self, type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, alter_color, alter_image_file, pos):
        super().__init__(type, rect_pos, rect_size, image_file, image_scaling, text_content, font, color, pos)
        if type == 'rect' or type == 'text':
            self.alter_color = alter_color
        elif type == 'image':
            self.alter_image_file = alter_image_file
            self.alter_image = pg.transform.scale(pg.image.load(self.alter_image_file).convert_alpha(), (self.image_scale))
        

    def Change_Color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.type == 'rect':
                pg.draw.rect(screen, self.alter_color, self.rect)

            if self.type == 'text':
                self.text = self.font.render(self.text_content, True, self.alter_color)
                screen.blit(self.text, self.rect)

            if self.type == 'image':
                screen.blit(self.alter_image, self.rect)
        else:
            if self.type == 'text':
                self.text = self.font.render(self.text_content, True, self.color)
                screen.blit(self.text, self.rect)

    
    def Mouse_Click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):  
            return True
        return False
    
    def Update(self, text_content, color, alter_color):
        if self.type == 'text':
            self.text_content = text_content
            self.color = color
            self.alter_color = alter_color
            self.text = self.font.render(self.text_content, True, self.color)

def Font(size):
    return pg.font.Font('font/arial.ttf', size)

class User_Data:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def Login(self):
        cur.execute("SELECT * FROM User_Data WHERE Username = ? AND Password = ?", (self.username, self.password))
        if cur.fetchall():
            return True
        else:
            return False

    def Sign_Up(self):
        cur.execute("INSERT INTO User_Data(Username, Password) VALUES (?,?)", (self.username, self.password))
        print(self.username)
        print(self.password)
        conn.commit()
        

pg.init()
if in_full_screen == 'False':   
    screen = pg.display.set_mode(start_screen_size, pg.SRCALPHA)
elif in_full_screen == 'True':
    screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.SRCALPHA)
