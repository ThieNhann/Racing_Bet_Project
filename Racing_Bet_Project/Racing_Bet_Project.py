import pygame
import random
import sys
import Experiment_Class as cls

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình
theme_list = ['ocean', 'forest', 'villager', 'street']
theme = 1
screen = pygame.display.set_mode((1280,720))
bg = pygame.image.load(f'Assets/background/{theme_list[theme]}.png').convert()
bg = pygame.transform.scale(bg, (1280,720))
fps = pygame.time.Clock()
size = cls.Screen_Info(screen.get_size())
class Char:
    def __init__(self, x, y, speed, image_path):
        self.x = x
        self.y = y
        self.speed = speed
        self.act_i = 0
        self.status = 'idle'
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
            self.walk[i]= pygame.transform.scale(self.walk[i], (50, 50))
            self.stun[i]= pygame.transform.scale(self.stun[i], (50, 50))
            if (i < 3):
                self.idle[i]= pygame.transform.scale(self.idle[i], (50, 50))
#        self.image = pygame.transform.scale(self.image, (50, 50))  # Thu nhỏ kích thước hình ảnh
        self.reverse = False
        self.teleport = False
        self.slow = False
        self.speedup = False
        self.effect_end_time = None
        self.wait_until = None  # Thời gian mà xe phải đợi trước khi di chuyển tiếp

    def draw(self,act_i,status):
        if status == 'walk':
            screen.blit(self.walk[act_i//15], (self.x, self.y))# Vẽ hình ảnh
        elif status == 'stun':
            screen.blit(self.stun[act_i//15], (self.x, self.y))
        else:
            screen.blit(self.idle[act_i//15], (self.x, self.y))
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
        self.status = 'walk'
        if self.reverse:
            self.x -= self.speed
        elif self.slow:
            self.x += self.speed / 2
        elif self.speedup:
            self.x += self.speed * 4
        else:
            self.x += self.speed

        if self.effect_end_time and pygame.time.get_ticks() > self.effect_end_time:
            self.reverse = False
            self.slow = False
            self.speedup = False
            self.effect_end_time = None
    
    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + 50 and self.y <= pos[1] <= self.y + 50

    def collides_with(self, obstacle):
        return self.x < obstacle.x + 50 and self.x + 50 > obstacle.x and self.y < obstacle.y + 50 and self.y + 50 > obstacle.y

# Tạo danh sách các xe với hình ảnh tương ứng
chars = [Char(50, 30 + (i + 1)*0.15*size.h, random.uniform(1, 2), f'Assets/char/animation/{theme_list[theme]}/{theme_list[theme]}_{i+1}') for i in range(5)]

class Obstacle:
    def __init__(self, x, y, image_paths):
        self.x = x
        self.y = y
        self.image_paths = image_paths
        self.set_image('Assets/Obstacles/obstacle_box.png')
        self.changed = False  # Thêm thuộc tính này để theo dõi xem hình ảnh đã được thay đổi chưa
        self.change_time = None  # Thêm thuộc tính này để theo dõi thời gian mà hình ảnh đã được thay đổi

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)  # Tải hình ảnh từ đường dẫn được cung cấp
        self.image = pygame.transform.scale(self.image, (50, 50))  # Thu nhỏ kích thước hình ảnh

    def set_random_image(self):
        if not self.changed:
            self.image_path = random.choice(self.image_paths)  # Lưu trữ hình ảnh hiện tại
            self.set_image(self.image_path)
            self.changed = True
            self.change_time = pygame.time.get_ticks()
            return self.image_path  # Trả về hình ảnh đã chọn

    def draw(self):
        screen.blit(self.image, (self.x, self.y))# Vẽ hình ảnh   
# Tạo danh sách các chướng ngại vật ở nửa đường
obstacle_images = ['Assets/Obstacles/obstacle_confinement.png', 'Assets/Obstacles/obstacle_finish.png', 
                   'Assets/Obstacles/obstacle_reverse.png', 'Assets/Obstacles/obstacle_slow.png', 
                   'Assets/Obstacles/obstacle_speed.png', 'Assets/Obstacles/obstacle_teleport.png', 
                   'Assets/Obstacles/obstacle_tostart.png']
obstacles = [Obstacle(random.uniform(size.w*0.3, size.w*0.7), 30 + 0.15*size.h*(i+1), obstacle_images) for i in range(5)]
# Hàm hiển thị menu và nhận lựa chọn từ người chơi
def show_menu():
    running = True
    while running:
        screen.blit(bg,(0,0))
        font = pygame.font.Font(None, 36)
        text = font.render("Choose your character!", True, (255, 255, 255))
        screen.blit(text, (250, 250))
        fps.tick(60)
        for char in chars:
            char.act_i = char.draw(char.act_i,char.status)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Thoát khỏi chương trình nếu người dùng đóng cửa sổ
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, char in enumerate(chars):
                    if char.is_clicked(pos):
                        return i  # Trả về chỉ số của xe mà người dùng đã chọn

# Hỏi người chơi chọn xe
player_choice = show_menu()

# Khởi tạo số vàng của người chơi
player_gold = 0

# Tạo một danh sách để theo dõi thứ tự các xe về đích
finish_order = []

# Vòng lặp chính của game
running = True
for char in chars:
    char.status = 'walk'
while running:
    # Xử lý các sự kiện
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(bg,(0,0))
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
                    char.wait_until = pygame.time.get_ticks() + 1000 # Đặt thời gian chờ cho xe
                    char.status = 'stun'
                elif 'obstacle_finish.png' in image_path:
                    char.x = 0.95*size.w
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
                    char.x += 200
                elif 'obstacle_tostart.png' in image_path:
                    char.x = 50

                    
        # Vẽ chướng ngại vật
        for obstacle in obstacles:
            obstacle.draw()

        # Loại bỏ các chướng ngại vật đã thay đổi hình ảnh từ hơn 2 giây trước
        obstacles = [obstacle for obstacle in obstacles if not obstacle.changed or pygame.time.get_ticks() - obstacle.change_time < 2000]

        # Cập nhật màn hình
        pygame.display.flip()

        # Kiểm tra xem có xe nào về đích chưa
        for i, char in enumerate(chars):
            if char.x >= size.w*0.95 and i not in finish_order:
                finish_order.append(i)
                char.speed = 0
                char.x = size.w*0.95
                char.status = 'idle'
                char.act_i = 0
                print(f"Xe số {i+1} đã về đích!")

        # Nếu tất cả các xe đều đã về đích, kết thúc trò chơi và công bố kết quả
        if len(finish_order) == len(chars):
            running = False
            print("Tất cả các xe đã về đích!")
            for i, char_index in enumerate(finish_order):
                if i == 0 and char_index == player_choice:
                    player_gold += 20
                    result_text = f"Your car comes first! You have received 20 gold. Your current gold amount is {player_gold}."
                else:
                    result_text = f"Car number {char_index+1} came in {i+1}th place."
        
                # Tạo font và vẽ văn bản lên màn hình
                font = pygame.font.Font(None, 36)
                text = font.render(result_text, True, (255, 255, 255))
                screen.blit(text, (250, 300 + i * 40))  # Thay đổi vị trí y để các dòng văn bản không chồng lên nhau

            # Cập nhật màn hình để hiển thị văn bản
            pygame.display.flip()

            # Đợi một chút trước khi thoát để người chơi có thể đọc kết quả
            pygame.time.wait(5000)
pygame.quit()