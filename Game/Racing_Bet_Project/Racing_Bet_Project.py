import pygame, sys
from pygame.locals import *

#tạo loop
def bg_dupe():
    DISPLAYSURF.blit(bg,(bg_xpos,0))
    DISPLAYSURF.blit(bg,(bg_xpos + wdw, 0))

pygame.init()

#khởi tạo window game
DISPLAYSURF = pygame.display.set_mode((1280, 720), RESIZABLE)
wdw0 = 1280
fps = pygame.time.Clock()
pygame.display.set_caption('GamblingRace')
bg = pygame.image.load('background\ocean\ocean.png')

bg_xpos = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    #scale background theo window
    (wdw, wdh) = DISPLAYSURF.get_size()
    bg = pygame.transform.scale(bg, (wdw, wdh))
    bg_speed = 1 * wdw/1280
    if (wdw != wdw0):
        bg_xpos *= wdw/wdw0
        wdw0 = wdw
    
    #thêm background vào game
    bg_xpos -= bg_speed
    bg_dupe()
    if bg_xpos <= -wdw:
        bg_xpos = 0
    pygame.display.update()
    fps.tick(120)
