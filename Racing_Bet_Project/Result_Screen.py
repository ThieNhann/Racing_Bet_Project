import pygame
import sys
import os
from Experiment_Class import *
#from PIL import Image
#import pyscreenshot as ImageGrab
import numpy as np 
import cv2 
import pyautogui 
from datetime import date, datetime
import math
import subprocess

# pygame.init()
def Show_Result(ranking_list, player_choice, game_theme, size, chars_list):
    theme_list = ["ocean", "forest", "villager", "street", "member"]
    theme = game_theme
    WIDTH, HEIGHT = size.w, size.h
    GOLD = (255, 215, 0)
    chr_select = player_choice + 1  # playera choose)
                    #1. bear   2.boar    3. deer   4.fox    5.wolf
    rank = ""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    class Stage:
        def __init__(self, name, width, height, color):
            self.name, self.width, self.height, self.color = name, width, height, color
            self.border_width, self.final_y, self.appear_delay, self.appeared = 4, HEIGHT, None, False

        def display(self, screen, x, y):
            border_rect = pygame.Rect(x - self.border_width, y - self.border_width,
                                    self.width + 2 * self.border_width, self.height + 2 * self.border_width)
            stage_rect = pygame.Rect(x, y, self.width, self.height)
            
            # Check if the stage number matches the rank and change the color accordingly
            if self.name.strip() == rank:
                pygame.draw.rect(screen, (255, 255, 0), stage_rect)  # Fill the stage with yellow
            else:
                pygame.draw.rect(screen, (100, 100, 100), border_rect)
                pygame.draw.rect(screen, (150, 150, 150), stage_rect)

            font = pygame.font.Font(None, 30)
            text = font.render(self.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
            screen.blit(text, text_rect)

            # Draw a smaller upside-down isosceles triangle above the player stand on the stage that has a number same as the rank
            if self.name.strip() == rank:
                triangle_top = (x + self.width // 2, y - 115 * size.h / 720)  # Bottom point of the triangle (moved higher by 150 pixels)
                triangle_left = (x + self.width // 3, y - 145 * size.h / 720)  # Left point of the base (moved higher by 150 pixels)
                triangle_right = (x + 2 * self.width // 3, y - 145 * size.h / 720)  # Right point of the base (moved higher by 150 pixels)
                pygame.draw.polygon(screen, (255, 255, 0), [triangle_top, triangle_left, triangle_right])  # Draw the triangle

    def load_images(directory, num_images):
        return [pygame.transform.scale(pygame.image.load(os.path.join(directory, f"walk_{i}.png")).convert_alpha(), (100 * size.w / 1280, 100 * size.h / 720)) for i in range(1, num_images + 1)]

    #change name, width(size), height of stage
    stage_info = [{"name": " 5th", "size": 256 * size.w / 1280, "height": 150 * size.h / 720}, {"name": " 4th", "size": 224 * size.w / 1280, "height": 225 * size.h / 720}, 
                {"name": " 3rd", "size": 192 * size.w / 1280, "height": 300 * size.h / 720}, {"name": " 2nd", "size": 160 * size.w / 1280, "height": 375 * size.h / 720}, 
                {"name": " 1st", "size": 128 * size.w / 1280, "height": 450 * size.h / 720}]

    sorted_stages = [Stage(info["name"], info["size"], info["height"], GOLD) for info in stage_info]

    pygame.display.set_caption("Stages")

    background_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets/background", f"{theme_list[theme]}.png")).convert(), (WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    spacing, running, animation_speed, delay_between_stages = 8, True, 5, 120

    baseSize = 100
    all_animations = [load_images(f"Assets/char/animation/{theme_list[theme]}/{theme_list[theme]}_{i}", 4) for i in range(1, 6)]
    for stage in sorted_stages: stage.appear_delay = sorted_stages.index(stage) * delay_between_stages

    frame_counter, player_frame_counters = 0, [0] * len(all_animations)
    show_player = [False] * len(sorted_stages)
    player_appear_time = [0] * len(sorted_stages)

    image_path = os.path.join("Assets/other", "result.png")  # Replace with the actual path to your image
    result_image = pygame.image.load(image_path).convert_alpha()
    congrats_image = pygame.image.load("Assets/other/congrat.png")
    # Create a surface with the screen dimensions and set its transparency
    black_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    black_surface.set_alpha(150) #higher is darker
    # Fill the surface with a semi-transparent black color
    black_surface.fill((0, 0, 0))  
    
    
    Next = Button('rect', (size.w*0.4, size.h * 0.9), (size.w*0.175, size.h * 0.075), None, None, None, None, '#FFFFFF', '#FFFFFF' , None, None)
    Next_text = Draw_to_Screen('text', None, None, None, None, 'Next', Font((40)), '#000000', Next.rect.center)

    player_order = ranking_list

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other events if needed

        # Display "RESULT" text at the top of the window
        screen.blit(background_image, (0, 0))
        # Display the black surface with opacity
        screen.blit(black_surface, (0, 0))
        # Display the loaded image at the top-left corner
        screen.blit(result_image, (0, 20)) 
        
        current_x, all_stages_appeared = (WIDTH - sum(stage.width for stage in sorted_stages) - (len(sorted_stages) - 1) * spacing) // 2, True

        all_stages_appeared = True
        for index, stage in enumerate(sorted_stages):
            if stage.final_y > HEIGHT - stage.height and stage.appear_delay <= 0:
                stage.final_y -= animation_speed
            elif stage.appear_delay > 0:
                stage.appear_delay -= 1
            
            if show_player[chr_select - 1] and stage.appeared and player_order[index] == chr_select:
                rank = stage.name.strip()  # Assign the stage's name to rank (remove any leading/trailing spaces)
            
            # Change the color of the stage that corresponds to the same number as rank to yellow
            if stage.name.strip() == rank:
                stage.color = (255, 255, 0)  # Change color to yellow

            stage.display(screen, current_x, stage.final_y)
            current_x += stage.width + spacing
            stage.appeared = stage.final_y <= HEIGHT - stage.height
            if not stage.appeared:
                all_stages_appeared = False

            player_index = player_order[index] - 1  # Adjust to 0-based index
            if stage.appeared and not show_player[player_index]:
                anim = all_animations[player_index]
                anim_frame = frame_counter // animation_speed % len(anim)
                anim_center_x = current_x - stage.width // 2 - anim[anim_frame].get_width() // 2
                anim_center_y = stage.final_y - 120 * size.h / 720
                screen.blit(anim[anim_frame], (anim_center_x, anim_center_y))
                player_frame_counters[player_index] += 1
                show_player[player_index] = True

            if stage.appeared and show_player[player_index]:
                anim = all_animations[player_index]
                anim_frame = frame_counter // animation_speed % len(anim)
                anim_center_x = current_x - stage.width // 2 - anim[anim_frame].get_width() // 2
                anim_center_y = stage.final_y - 120 * size.h / 720
                screen.blit(anim[anim_frame], (anim_center_x, anim_center_y))
                player_frame_counters[player_index] += 1
        
        # Display chr_select and rank at the top-right corner
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Your rank: {rank}", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topright = (WIDTH - 20, 20)  
        screen.blit(text_surface, text_rect)
        
            # Check if the rank is 1 and display congratulatory message at the center
        if rank == "1":
            # Display congratsz mess
            congrats_rect = congrats_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            screen.blit(congrats_image,congrats_rect)
        frame_counter += 1
        
        if all_stages_appeared:
            Next.Blit(0,0)
            Next_text.Blit(0,0)
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN):
                        pos = pygame.mouse.get_pos()
                        if Next.Click(pos):
                            running = False
        pygame.display.flip()
        clock.tick(60)
        
    rank_list = ['1st', '2nd', '3rd', '4th', '5th']
    
    Result_text = Draw_to_Screen('text', None, None, None, None, 'RESULT', Font((70)), '#FFFFFF', (size.w * 0.1, size.h * 0.1))
    for i in range(5):
        j = ranking_list[i] - 1
        char = chars_list[j]
        rank = 5 - i - 1
        char.rank = rank
        char.rank_display = Draw_to_Screen('text', None, None, None, None, f'{char.name} : {rank_list[rank]} place', Font((25)), '#FFFFFF', (0,0))
        char.rank_display.rect.center = (size.w * 0.1325, size.h * (0.225 + 0.14 * rank))
        if j == player_choice:
            char.player_chose = Draw_to_Screen('text', None, None, None, None, "Chosen by player", Font((25)), '#e8bd3d', (size.w * 0.425, size.h * (0.2 + 0.15 * rank)))
        else:
            char.player_chose = Draw_to_Screen('text', None, None, None, None, "", Font((25)), '#FFFFFF', (size.w * 0.4, size.h * (0.2 + 0.15 * rank)))
    horizontal_lines = [Draw_to_Screen('rect', (size.w * 0, size.h * (0.15 + 0.1415 * i)), (size.w * 0.6, size.h * 0.005), None, None, None, None, '#ffffff', None) for i in range(7)]
    vertical_lines = []
    vertical_lines.append(Draw_to_Screen('rect', (size.w * 0, size.h * 0.15), (size.w * 0.005, size.h * 0.75), None, None, None, None, '#ffffff', None))
    vertical_lines.append(Draw_to_Screen('rect', (size.w * 0.25, size.h * 0.15), (size.w * 0.005, size.h * 0.75), None, None, None, None, '#ffffff', None))
    vertical_lines.append(Draw_to_Screen('rect', (size.w * 0.6025, size.h * 0.15), (size.w * 0.005, size.h * 0.75), None, None, None, None, '#ffffff', None))
    test = pg.surface.Surface((size.w * 0.6125, size.h * 0.86))
    test.set_alpha(150)
    test.fill(0)
    running = True
    while running:
        screen.fill(0)

        screen.blit(background_image, (0, 0))
        screen.blit(black_surface, (0, 0))

        Result_text.Con_Blit(test,0,0)

        for char in chars_list:
            char.rank_display.Con_Blit(test,0,0)
            char.player_chose.Con_Blit(test,0,0)
            test.blit(char.idle[1], (size.w * 0.6, size.h * (0.15 + 0.15 * char.rank)))

        Next.Blit(0,0)
        Next_text.Blit(0,0)

        for line in horizontal_lines:
            line.Con_Blit(test, 0,0)
        for line in vertical_lines:
            line.Con_Blit(test, 0,0)

        screen.blit(test, (size.w * 0.175, size.h * 0.05))



        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    if Next.Click(pos):
                        running = False
                        now = datetime.now()
                        current_time = now.strftime("%H-%M-%S")
                        today = date.today()
#                        bbox = (math.floor(size.w * 0.18), math.floor(size.h * 0.15), math.floor(size.w * (0.18 + 0.605)), math.floor(size.h * (0.15 + 0.755)))
#                        region_screenshot = ImageGrab.grab(bbox=bbox)
#                        region_screenshot.save(f'screenshot/screenshot_{current_time}_{today}.png')
                        screenshot = pyautogui.screenshot(region = (math.floor(size.w * 0.18), math.floor(size.h * 0.15), math.floor(size.w * 0.605), math.floor(size.h * 0.755))) 
                        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                        cv2.imwrite(f'screenshot/screenshot_{current_time}_{today}.png', screenshot) 
                        pg.image.save(test, 'balls.png')
                        subprocess.run(["python", "convert.py"])
                        
                        return
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()