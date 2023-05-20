import pygame
import random
from time import sleep
from pygame import mixer

pygame.mixer.init()
pygame.mixer.music.load('.\\music\\background.wav')
pygame.mixer.music.play(-1) 

class Car:
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.game_display = None

        self.initialize()

    def initialize(self):

        self.crashed = False
        
        # personal car
        self.carImg = pygame.image.load('.\\images\\car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy car
        self.enemy_car = pygame.image.load('.\\images\\enemy_car_1.png')
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load(".\\images\\back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.game_display.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def running_window(self):
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        self.run_car()

    def run_car(self):
        
        self.explosion_sound = pygame.mixer.Sound('.\\music\\explosion.wav')
        pygame.mixer.music.play(-1)  

        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_coordinate -= 50
                    if event.key == pygame.K_RIGHT:
                        self.car_x_coordinate += 50

            self.game_display.fill(self.black)
            self.background_road()

            self.enemy_car_running(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.score(self.count)
            self.count += 1

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if (
                    self.car_x_coordinate > self.enemy_car_startx
                    and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width
                ) or (
                    self.car_x_coordinate + self.car_width > self.enemy_car_startx
                    and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width
                ):
                    self.crashed = True

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True

            pygame.display.update()
            self.clock.tick(60)

        pygame.mixer.music.stop()  
        self.explosion_sound.play()
        self.display_message("Game Over")
        self.explosion_sound.stop()  
        self.initialize()  
        self.running_window()

    def display_message(self, msg):
        font = pygame.font.SysFont("arial", 75, True)
        text = font.render(msg, True, (255, 255, 255))
        self.game_display.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Play Again
                        self.initialize()
                        self.running_window()
                    elif event.key == pygame.K_ESCAPE:  # Exit the Game
                        pygame.quit()
                        sys.exit()

    
    def background_road(self):
        self.game_display.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.game_display.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def enemy_car_running(self, thingx, thingy):
        self.game_display.blit(self.enemy_car, (thingx, thingy))

    def score(self, count):
        font = pygame.font.SysFont("arial", 50)
        text = font.render("Score : " + str(count), True, self.white)
        self.game_display.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("arial", 20)

if __name__ == '__main__':
    car_racing = Car()
    car_racing.running_window()