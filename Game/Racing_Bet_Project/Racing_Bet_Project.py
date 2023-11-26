import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình
screen = pygame.display.set_mode((800,600))
bg = pygame.image.load('Assets/background/ocean/ocean.png').convert()
bg = pygame.transform.scale(bg, (800, 600)) 
class Car:
    def __init__(self, x, y, speed, image_path):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)  # Tải hình ảnh từ đường dẫn được cung cấp
        self.image = pygame.transform.scale(self.image, (50, 50))  # Thu nhỏ kích thước hình ảnh
        self.reverse = False
        self.teleport = False
        self.slow = False
        self.speedup = False
        self.effect_end_time = None
        self.wait_until = None  # Thời gian mà xe phải đợi trước khi di chuyển tiếp

    def draw(self):
        screen.blit(self.image, (self.x, self.y))  # Vẽ hình ảnh thay vì hình vuông
        
    def move(self):
        if self.wait_until and pygame.time.get_ticks() < self.wait_until:
            return  # Nếu xe đang trong thời gian chờ, không di chuyển nó
        if self.reverse:
            self.x -= self.speed
        elif self.slow:
            self.x += self.speed / 2
        elif self.speedup:
            self.x += self.speed * 2
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
cars = [Car(50, i*100 + 50, random.uniform(0.01, 0.05), f'Assets/char/still/ocean/ocean{i+1}.png') for i in range(5)]

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
        screen.blit(self.image, (self.x, self.y))  # Vẽ hình ảnh
    
# Tạo danh sách các chướng ngại vật ở nửa đường
obstacle_images = ['Assets/Obstacles/obstacle_confinement.png', 'Assets/Obstacles/obstacle_finish.png', 'Assets/Obstacles/obstacle_reverse.png', 'Assets/Obstacles/obstacle_slow.png', 'Assets/Obstacles/obstacle_speed.png', 'Assets/Obstacles/obstacle_teleport.png', 'Assets/Obstacles/obstacle_tostart.png']
obstacles = [Obstacle(400, i*100 + 50, obstacle_images) for i in range(5)]
# Hàm hiển thị menu và nhận lựa chọn từ người chơi
def show_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Choose your character!", True, (255, 255, 255))
        screen.blit(text, (250, 250))
        for car in cars:
            car.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Thoát khỏi chương trình nếu người dùng đóng cửa sổ
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, car in enumerate(cars):
                    if car.is_clicked(pos):
                        return i  # Trả về chỉ số của xe mà người dùng đã chọn

# Hỏi người chơi chọn xe
player_choice = show_menu()

# Khởi tạo số vàng của người chơi
player_gold = 0

# Vòng lặp chính của game
running = True
while running:
    # Xử lý các sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(bg,(0,0))
        # Vẽ và di chuyển các xe
        for car in cars:
            car.draw()
            car.move()
            image_path = None  # Khởi tạo image_path với giá trị mặc định
            for obstacle in obstacles:
                if car.collides_with(obstacle):
                    image_path = obstacle.set_random_image()  # Lấy hình ảnh đã chọn
            if image_path:  # Kiểm tra nếu image_path không phải là None
        
                if 'obstacle_confinement.png' in image_path:  # Kiểm tra hình ảnh hiện tại của chướng ngại vật
                    car.wait_until = pygame.time.get_ticks() + 3000  # Đặt thời gian chờ cho xe
                elif 'obstacle_finish.png' in image_path:
                    car.x = 750
                elif 'obstacle_reverse.png' in image_path:
                    car.reverse = True
                    car.effect_end_time = pygame.time.get_ticks() + 3000
                elif 'obstacle_slow.png' in image_path:
                    car.slow = True
                    car.effect_end_time = pygame.time.get_ticks() + 3000
                elif 'obstacle_speed.png' in image_path:
                    car.speedup = True
                    car.effect_end_time = pygame.time.get_ticks() + 3000
                elif 'obstacle_teleport.png' in image_path:
                    car.x += 100
                elif 'obstacle_tostart.png' in image_path:
                    car.x = 50

                    
        # Vẽ chướng ngại vật
        for obstacle in obstacles:
            obstacle.draw()

        # Loại bỏ các chướng ngại vật đã thay đổi hình ảnh từ hơn 2 giây trước
        obstacles = [obstacle for obstacle in obstacles if not obstacle.changed or pygame.time.get_ticks() - obstacle.change_time < 2000]

        # Cập nhật màn hình
        pygame.display.flip()

        # Kiểm tra xem có xe nào về đích chưa
        for i, car in enumerate(cars):
            if car.x >= 750:
                print(f"Xe số {i+1} đã về đích!")
                if i == player_choice:
                    player_gold += 20
                    print(f"Chúc mừng! Xe của bạn đã về đích đầu tiên! Bạn đã nhận được 20 vàng. Số vàng hiện tại của bạn là {player_gold}.")
                else:
                    font = pygame.font.Font(None, 72)
                    text = font.render("Game Over", True, (255, 0, 0))
                    screen.blit(text, (350, 300))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                running = False        
pygame.quit()
    