import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "JackRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "JackRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "grass.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 320
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.hitbox = pygame.Rect(self.dino_rect.x + 12, self.dino_rect.y + 10, 40, 50)

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        if userInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.hitbox = pygame.Rect(self.dino_rect.x + 12, self.dino_rect.y + 20, 30, 50)
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.hitbox = pygame.Rect(self.dino_rect.x + 12, self.dino_rect.y + 20, 30, 50)
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 1
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        self.hitbox = pygame.Rect(self.dino_rect.x + 12, self.dino_rect.y + 10, 33, 30)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Background:
    def __init__(self):


        self.image = pygame.image.load(os.path.join("Assets/BG", "test.png"))


        self.image_width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.image_width
        self.y = 5

    def update(self):
        self.x1 -= game_speed // 4
        self.x2 -= game_speed // 4
        if self.x1 <= -self.image_width:
            self.x1 = self.x2 + self.image_width
        if self.x2 <= -self.image_width:
            self.x2 = self.x1 + self.image_width

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x1, self.y))
        SCREEN.blit(self.image, (self.x2, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.hitbox = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)

    def update(self):
        self.rect.x -= game_speed
        self.hitbox.x = self.rect.x + 5
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.hitbox = pygame.Rect(self.rect.x + 100, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        self.hitbox = pygame.Rect(self.rect.x + 100, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 270
        self.index = 0
        self.hitbox = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width - 5, self.rect.height - 5)

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)
        self.index += 1

class coins():
    def __init__(self):
        self.image = pygame.image.load(os.path.join("Assets/BG", "bulb.png"))

        self.image_width = self.image.get_width()
        self.x1 = 100
        self.x2 = self.image_width
        self.y = 250


    def update(self):
        pass
        # Coins = coins()
        # dino = Dinosaur()
        #
        # for c in Coins:
        #     if c.colliderect(dino):
        #         Coins.remove(c)


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x1, self.y))



def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    background_img = Background()
    points = 0
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    Coins = coins()

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        SCREEN.blit(text, (1000, 40))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        background_img.draw(SCREEN)
        background_img.update()
        background()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            choice = random.randint(0, 2)
            if choice == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif choice == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))


        Coins.draw(SCREEN)
        Coins.update()
        coins()

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.hitbox.colliderect(obstacle.hitbox):
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        else:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            SCREEN.blit(score, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))

        SCREEN.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
