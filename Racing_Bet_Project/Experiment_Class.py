import pygame as pg

class Screen_Info:
    def __init__(self, current_size):
        self.w, self.h = current_size
        print(True)

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
        self.image = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/Circle.png').convert_alpha(), 0, 0.005 * self.r)
        self.rect = self.image.get_rect(center = (self.pos))
    
    def Kill(self):
        if self.r >= 75 * self.size/1280:
            self.kill()
        
    def update(self):
        self.r += 1.5 * self.size/1280
        self.transparency -= 255 * (1.75 / 70)
        self.image = pg.transform.rotozoom(pg.image.load('Assets/icon/Settings/Circle.png').convert_alpha(), 0, 0.005 * self.r)
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
        self.rect = self.image.get_rect(center = (self.x + 0.06 * self.mouse_x, self.y + 0.06 * self.mouse_y))
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

    def Update(self, new_pos):

        if self.type == 'image':
            self.x, self.y = new_pos

        if self.type == 'text':
            self.x, self.y = new_pos
        
        if self.type == 'rect':
            self.x, self.y = new_pos
        
        self.Blit()
      
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
            elif self.type != 'text' and self.type != 'image':
                pg.draw.rect(screen, self.color, self.rect)

            if self.type == 'text':
                self.text = self.font.render(self.text_content, True, self.alter_color)
                screen.blit(self.text, self.rect)

            elif self.type != 'rect' and self.type != 'image':
                self.text = self.font.render(self.text_content, True, self.color)
                screen.blit(self.text, self.rect)
            
            if self.type == 'image':
                screen.blit(self.alter_image, self.rect)
            elif self.type != 'rect' and self.type != 'text':
                screen.blit(self.image, self.rect)
    
    def Mouse_Click(self, mouse_pos):
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

def Font(size):
    return pg.font.Font(None, size)

pg.init()
screen = pg.display.set_mode((1280, 720), pg.SRCALPHA)