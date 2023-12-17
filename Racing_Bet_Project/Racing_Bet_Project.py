import pygame
import random
import sys
import os
from Experiment_Class import *
import Result_Screen as result
import subprocess



# Khởi tạo Pygame
pygame.init()
# Thiết lập kích thước màn hình
theme_list = ['ocean', 'forest', 'villager', 'street', 'member']

something = random.randint(1, 10101010101);
THE_MOST_NORMAL_CAT = 'Cat is me. Literally me. No other animal can come close to relating to me like this. There is no way you can convince me this is not me. Cat could not possibly be anymore me. It is me, and nobody can convince me otherwise. If anyone approached me on the topic of this not possibly being me, then I immediately shut them down with overwhelming evidence that this animal is me. This animal is me, it is indisputable. Why anyone would try to argue that this animal is not me is beyond me. If you held two pictures of me and the cat side by side, you would see no difference. I can safely look at this chart every day and say "Yup, that is me". I can practically see this animal every time I look at myself in the mirror. I go outside and people stop me to comment how similar I look and act to this animal. I chuckle softly as I am assured everyday this animal is me in every way. I can smile each time I get out of bed every morning knowing that I have found my identity with this animal and I know my place in this world. It is really quite funny how similiar the cat is to me. It is almost like we are identical twins. When I first saw the cat, I had an existential crisis. What if this animal was the real me and I was the fictional being. What if this animal actually became aware of my existence? Did it have the ability to become self aware itself?'
    
name_list = ['ThieNhann', 'Lackiem1707', 'phuc-dep-trai', 'dzqt1', 'Nichikou']

names = ['Kevin','Alberto','Carol','Claire','Chris','Henrietta','Sophie','Jane','Candace','Tom',
             'Lowell','Myrtle','Dana','Rosa','Byron','Ramon','Bryan','Dale','Matthew','Malcolm',
             'Terrance','Lynn','Edith','Rodolfo','Antonia','Hector','Meredith','Vernon','Tami','Vicky',
             'Eddie','Julio','Tonya','Wilbert','Vickie','Betsy','Jaime','Leigh','Walter','Loretta',
             'Susie','Rodney','Grace','Kyle','Rachael','Bryant','Erika','Shelia','Kristi','Harry']



name_set = random.sample(range(0, 49), 5)

theme = 4
length = 0
baseSize = 90
baseSpeed = 10 # thay đổi speed nhân vật (for testing)
screen = pygame.display.set_mode((1280, 720))
bg = pygame.image.load(f'Assets/background/{theme_list[theme]}.png').convert()
bg = pygame.transform.scale(bg, (1280,720))
fps = pygame.time.Clock()
size = Screen_Info(screen.get_size())

crown = []
for i in range(8):
    image = pygame.image.load(f"Assets/other/crown/frame_{i}_delay-0.2s.gif").convert()
    image = pygame.transform.scale(image, (40 * size.w / 1280, 40 * size.h / 720))
    crown.append(image)

class Char:
    def __init__(self, x, y, speed, name, image_path):
        self.x = x
        self.y = y
        if theme == 4:
            self.y += 0.05 * size.h
        self.speed = speed
        self.name = name
        self.act_i = 0
        self.crown_i = 0
        self.status = 'idle'
        self.laps = 0
        self.orientation = 1
        self.baseY = self.y
        self.laps_display = Draw_to_Screen('text', None, None, None, None, f'{self.laps}/{length}', Font((40)), '#FFFFFF', (self.x - 20 * size.w / 1280, self.y + 20 * size.h / 720))
        if theme == 3:
            self.name_display = Draw_to_Screen('text', None, None, None, None, f'{self.name}', Font((40)), '#FFFFFF', (self.x + 40 * size.w / 1280, self.y + 0.15 * size.h))
        else:
            self.name_display = Draw_to_Screen('text', None, None, None, None, f'{self.name}', Font((40)), '#FFFFFF', (self.x + 40 * size.w / 1280, self.y + 0.1 * size.h))
        self.rank_display = Draw_to_Screen('text', None, None, None, None, "", Font((40)), '#FFFFFF', (0,0))
        self.player_chose = Draw_to_Screen('text', None, None, None, None, "", Font((40)), '#FFFFFF', (0,0))
        # Tải hình ảnh từ đường dẫn được cung cấp
        self.walk = [pygame.image.load(image_path + f'/walk_1.png'),
                     pygame.image.load(image_path + f'/walk_2.png'),
                     pygame.image.load(image_path + f'/walk_3.png'),
                     pygame.image.load(image_path + f'/walk_4.png')]
        self.stun = [pygame.image.load(image_path + f'/death_1.png'),
                     pygame.image.load(image_path + f'/death_2.png'),
                     pygame.image.load(image_path + f'/death_3.png'),
                     pygame.image.load(image_path + f'/death_4.png')]
        self.idle = [pygame.image.load(image_path + f'/idle_1.png'),
                     pygame.image.load(image_path + f'/idle_2.png'),
                     pygame.image.load(image_path + f'/idle_3.png')]
        for i in range(4):
            self.walk[i]= pygame.transform.scale(self.walk[i], (baseSize * size.w / 1280, baseSize * size.h / 720))
            self.stun[i]= pygame.transform.scale(self.stun[i], (baseSize * size.w / 1280, baseSize * size.h / 720))
            if (i < 3):
                self.idle[i]= pygame.transform.scale(self.idle[i], (baseSize * size.w / 1280, baseSize * size.h / 720))
#        self.image = pygame.transform.scale(self.image, (50, 50))  # Thu nhỏ kích thước hình ảnh
        self.reverse = False
        self.teleport = False
        self.slow = False
        self.speedup = False
        self.finished = False
        self.first_finish = False
        self.effect_end_time = None
        self.wait_until = None  # Thời gian mà xe phải đợi trước khi di`` chuyển tiếp

    def draw(self,act_i,status):
        if status == 'walk':
            if self.orientation == 1:
                screen.blit(self.walk[act_i//15], (self.x, self.y)) # Vẽ hình ảnh
            elif self.orientation == -1:
                screen.blit(pygame.transform.flip(self.walk[act_i//15],1,0), (self.x, self.y))
        elif status == 'stun':
            if self.orientation == 1:
                screen.blit(self.stun[act_i//15], (self.x, self.y)) # Vẽ hình ảnh
            elif self.orientation == -1:
                screen.blit(pygame.transform.flip(self.stun[act_i//15],1,0), (self.x, self.y))
        else:
            if self.orientation == 1:
                screen.blit(self.idle[act_i//15], (self.x, self.y)) # Vẽ hình ảnh
            elif self.orientation == -1:
                screen.blit(pygame.transform.flip(self.idle[act_i//15],1,0), (self.x, self.y))
        if status == 'idle':
            if act_i == 44:
                return 0
            else:
                return act_i+1
        else:
            if act_i == 59:
                if status == 'stun':
                    return act_i
                else:   
                    return 0
            else:
                return act_i+1  # Vẽ hình ảnh thay vì hình vuông
        
    def move(self):
        if self.wait_until and pygame.time.get_ticks() < self.wait_until:
            self.status = 'stun'
            return  # Nếu xe đang trong thời gian chờ, không di chuyển nó
        if not self.finished:
            self.status = 'walk'
        if self.reverse:
            self.x -= self.speed
            self.orientation = -(self.speed/abs(self.speed))
        elif self.slow:
            self.x += self.speed / 2
        elif self.speedup:
            self.x += self.speed * 3
        else:
            self.x += self.speed
        
        if not (self.reverse or self.finished):
            char.orientation = char.speed/abs(char.speed)
        
        if self.effect_end_time and pygame.time.get_ticks() > self.effect_end_time:
            self.reverse = False
            self.slow = False
            self.speedup = False
            self.effect_end_time = None
             
        if self.first_finish:
            if self.act_i % 15 == 0:
                if self.crown_i == 7:
                    self.crown_i = 0
                else:
                    self.crown_i += 1
            screen.blit(crown[self.crown_i], (self.x + 30 * size.w / 1280, self.y - 20 * size.h / 720))
                
        
    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + baseSize * size.w / 1280 and self.y <= pos[1] <= self.y + baseSize * size.h / 720

    def collides_with(self, obstacle):
        return self.x < obstacle.x + baseSize * size.w / 1280 and self.x + baseSize * size.w / 1280 > obstacle.x and self.y < obstacle.y + baseSize * size.h / 720 and self.y + baseSize * size.h / 720 > obstacle.y

# Tạo danh sách các xe với hình ảnh tương ứng
if theme == 4:
    chars = [Char(50, 30 + (i + 1)*0.15*size.h, random.uniform(baseSpeed * 1,baseSpeed * 2) * size.w / 1280, name_list[i], f'Assets/char/animation/{theme_list[theme]}/{theme_list[theme]}_{i+1}')  for i in range(5)]
else:
    chars = [Char(50, 30 + (i + 1)*0.15*size.h, random.uniform(baseSpeed * 1,baseSpeed * 2) * size.w / 1280, names[name_set[i]], f'Assets/char/animation/{theme_list[theme]}/{theme_list[theme]}_{i+1}')  for i in range(5)]

if theme == 3 and something == 727:
    chars[1].name = THE_MOST_NORMAL_CAT

class Obstacle:
    def __init__(self, x, y, image_paths):
        self.x = x
        self.y = y
        if theme == 4:
            self.y += 0.05 * size.h
        self.image_paths = image_paths
        self.set_image('Assets/Obstacles/obstacle_box.png')
        self.changed = False  # Thêm thuộc tính này để theo dõi xem hình ảnh đã được thay đổi chưa
        self.change_time = None  # Thêm thuộc tính này để theo dõi thời gian mà hình ảnh đã được thay đổi

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)  # Tải hình ảnh từ đường dẫn được cung cấp
        self.image = pygame.transform.scale(self.image, (baseSize * size.w / 1280, baseSize * size.h / 720))  # Thu nhỏ kích thước hình ảnh

    def set_random_image(self):
        rare_chance = 5     # Điều chỉnh tỉ lệ obstacle to_start và to_finish (1 = 0.1%)   (phần còn lại chia đều)
        if not self.changed:
            image_picker = random.randint(1, 1000)
            if image_picker <= rare_chance:
                self.image_path = self.image_paths[5]
            elif image_picker > 1000 - rare_chance:
                self.image_path = self.image_paths[6]
            else:
                self.image_path = self.image_paths[image_picker % 5]

            #self.image_path = random.choice(self.image_paths)  # Lưu trữ hình ảnh hiện tại
            self.set_image(self.image_path)
            self.changed = True
            self.change_time = pygame.time.get_ticks()
            return self.image_path  # Trả về hình ảnh đã chọn

    def draw(self):
        screen.blit(self.image, (self.x, self.y))# Vẽ hình ảnh   
# Tạo danh sách các chướng ngại vật ở nửa đường
obstacle_images = ['Assets/Obstacles/obstacle_confinement.png',  
                   'Assets/Obstacles/obstacle_reverse.png', 'Assets/Obstacles/obstacle_slow.png', 
                   'Assets/Obstacles/obstacle_speed.png', 'Assets/Obstacles/obstacle_teleport.png', 
                   'Assets/Obstacles/obstacle_tostart.png', 'Assets/Obstacles/obstacle_finish.png']
obstacles = [Obstacle(random.uniform(size.w*0.3, size.w*0.7), 30 + 0.15*size.h*(i+1), obstacle_images) for i in range(5)]
# Hàm hiển thị menu và nhận lựa chọn từ người chơi
def show_menu():
    running = True
    selection = -1
    player_name = ''
    rename = False
    charImage = Draw_to_Screen('text', None, None, None, None, '', 
                                    Font(int(50 * size.w / 1280)), '#FFFFFF', (size.w * 0.60, size.h * 0.5))
    rename_box = Button('rect', (size.w * 0.35, size.h * 0.7), (size.w*0.275, size.h * 0.1), None, None, None, None, '#FFFFFF', '#FFFFFF', None, None)
    if theme == 4:
        charname_text = Draw_to_Screen('text', None, None, None, None, "Your character name (please don't change it):", Font((60)), '#FFFFFF', (size.w * 0.5, size.h * 0.65)) 
    else:
        charname_text = Draw_to_Screen('text', None, None, None, None, 'Choose your character name:', Font((60)), '#FFFFFF', (size.w * 0.5, size.h * 0.65)) 
    while running:
        screen.blit(bg,(0,0))
        font = pygame.font.Font(None, 36)
        text = Draw_to_Screen('text', None, None, None, None, 'Choose your character!', 
                    Font(int(70 * size.w / 1280)), '#FFFFFF', (size.w * 0.5, size.h * 0.3))
        
        currentChar = Draw_to_Screen('text', None, None, None, None, 'Your character:', 
                    Font(int(50 * size.w / 1280)), '#FFFFFF', (size.w * 0.4, size.h * 0.5))
        
        Start = Button('rect', (size.w*0.4, size.h * 0.85), (size.w*0.175, size.h * 0.075), None, None, None, None, '#FFFFFF', '#FFFFFF' , None, None)
        Start_text = Draw_to_Screen('text', None, None, None, None, 'Start', Font((40)), '#000000', Start.rect.center)
        
        rename_text = Draw_to_Screen('text', None, None, None, None, player_name, Font((40)), '#000000', rename_box.rect.center)
        
        text.Blit(0,0)
        currentChar.Blit(0,0)
        charImage.Blit(0,0)
        Start.Blit(0,0)
        Start_text.Blit(0,0)
        rename_box.Blit(0,0)
        rename_text.Blit(0,0)
        charname_text.Blit(0,0)
        
        fps.tick(60)
        for char in chars:
            char.act_i = char.draw(char.act_i,char.status)
            char.name_display.Blit(0,0)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Thoát khỏi chương trình nếu người dùng đóng cửa sổ
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, char in enumerate(chars):
                    if char.is_clicked(pos):
                        charImage = Draw_to_Screen('image', None, None, f'Assets/char/animation/{theme_list[theme]}/{theme_list[theme]}_{i+1}/idle_1.png', ((baseSize * 1.2)*size.w/1280, (baseSize * 1.2)* size.w/1280), None, 
                                    None, None, (size.w * 0.6, size.h * 0.5))
                        player_name = char.name
                        selection = i                # Trả về chỉ số của xe mà người dùng đã chọn
                    if Start.Click(pos) and selection != -1:
                        if rename and player_name != '':
                            chars[selection].name = player_name
                        return selection
                    if rename_box.Click(pos) and theme != 4:
                        rename = True
                        
            if event.type == pygame.KEYDOWN:
                if rename:
                    if event.key == pg.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                        
                

# Hỏi người chơi chọn xe
player_choice = show_menu()

# Khởi tạo số vàng của người chơi
player_gold = 0

# Tạo một danh sách để theo dõi thứ tự các xe về đích
finish_order = []
ranking_list = []

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    if Finish.Click(pos):
                        running = False
                        result.Show_Result(ranking_list, player_choice, theme, size, chars)
        screen.blit(bg,(0,0))
        if all_Finish:
            Finish.Blit(0,0)
            Finish_text.Blit(0,0)
        
        # Vẽ và di chuyển các xe
        for char in chars:
            char.act_i = char.draw(char.act_i, char.status)
            char.move()
            char.laps_display = Draw_to_Screen('text', None, None, None, None, f'{char.laps}/{length+1}', Font((20)), '#FFFFFF', (char.x - 15 * size.w / 1280, char.y + 20 * size.h / 720))
            if theme == 3:
                char.name_display = Draw_to_Screen('text', None, None, None, None, f'{char.name}', Font((40)), '#FFFFFF', (char.x + 40 * size.w / 1280, char.y + 0.15 * size.h))
            else:
                char.name_display = Draw_to_Screen('text', None, None, None, None, f'{char.name}', Font((40)), '#FFFFFF', (char.x + 40 * size.w / 1280, char.y + 0.1 * size.h))
            char.laps_display.Blit(0,0)
            char.name_display.Blit(0,0)
            image_path = None  # Khởi tạo image_path với giá trị mặc định
            for obstacle in obstacles:
                if char.collides_with(obstacle):
                    image_path = obstacle.set_random_image()  # Lấy hình ảnh đã chọn
            if image_path:  # Kiểm tra nếu image_path không phải là None
        
                if 'obstacle_confinement.png' in image_path:  # Kiểm tra hình ảnh hiện tại của chướng ngại vật
                    char.wait_until = pygame.time.get_ticks() + 1000 # Đặt thời gian chờ cho xe
                    char.status = 'stun'
                elif 'obstacle_finish.png' in image_path:
                    if (length % 2 == 0):
                        char.x = 0.92 * size.w
                        char.orientation = 1
                    else:
                        char.x = 0.05 * size.w
                        char.orientation = -1
                    char.laps = length
                elif 'obstacle_reverse.png' in image_path:
                    char.reverse = True
                    char.effect_end_time = pygame.time.get_ticks() + 1000
                elif 'obstacle_slow.png' in image_path:
                    char.slow = True
                    char.effect_end_time = pygame.time.get_ticks() + 1000
                elif 'obstacle_speed.png' in image_path:
                    char.speedup = True
                    char.effect_end_time = pygame.time.get_ticks() + 500
                elif 'obstacle_teleport.png' in image_path:
                    char.x += char.speed/(abs(char.speed)) * 200 * size.w / 1280
                elif 'obstacle_tostart.png' in image_path:
                    char.x = 0.05 * size.w
                    char.laps = 0
                    char.speed = abs(char.speed)
                    char.orientation = 1
                                    
        # Vẽ chướng ngại vật
        for obstacle in obstacles:
            obstacle.draw()

        # Loại bỏ các chướng ngại vật đã thay đổi hình ảnh từ hơn 2 giây trước
        obstacles = [obstacle for obstacle in obstacles if not obstacle.changed or pygame.time.get_ticks() - obstacle.change_time < 2000]

        # Cập nhật màn hình
        pygame.display.flip()

        # Kiểm tra xem có xe nào về đích chưa
        for i, char in enumerate(chars):
            if (char.x >= 0.92*size.w and char.laps % 2 == 0) or (char.x <= 0.05*size.w and char.laps % 2 == 1):
                if char.laps == length and i not in finish_order:
                    if len(finish_order) == 0:
                        char.first_finish = True
                    finish_order.append(i)
                    ranking_list.insert(0, i + 1)
                    print(ranking_list)
                    char.speed = 0
                    if length % 2 == 0:
                        char.x = size.w*0.92
                    else:
                        char.x = size.w*0.05
                    char.status = 'idle'
                    char.act_i = 0
                    char.laps += 1
                    char.finished = True
                    char.laps_display = Draw_to_Screen('text', None, None, None, None, f'{char.laps}/{length+1}', Font((40)), '#FFFFFF', (char.x - 30 * size.w / 1280, char.y))
                    print(f"Char {i+1} finished!")
                elif not char.finished:
                    obstacles.append(Obstacle(random.uniform(size.w*0.3, size.w*0.7), 30 + 0.15*size.h*(i+1), obstacle_images))
                    char.laps += 1
                    char.speed = -1*char.speed

        
        # Nếu tất cả các xe đều đã về đích, kết thúc trò chơi và công bố kết quả
        if len(finish_order) == len(chars):
            all_Finish = True
pygame.quit()