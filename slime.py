import pygame
import os
import random
pygame.init()
from pygame import mixer


SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Player", "JackRun1.png")),
           pygame.image.load(os.path.join("Assets/Player", "JackRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Player", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Player", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Player", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Obstacle", "SmallObstacle1.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "SmallObstacle2.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "SmallObstacle3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Obstacle", "LargeObstacle1.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "LargeObstacle2.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "LargeObstacle3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

NOTE = pygame.image.load(os.path.join("Assets/Other", "note.png"))
BG = pygame.image.load(os.path.join("Assets/Background", "Ground.png"))

MENU_BG = pygame.image.load(os.path.join("Assets/Background", "DesertHills_Main.png"))


JUMP_SFX = pygame.mixer.Sound(os.path.join("Assets/sounds", "jump.wav"))
JUMP_SFX.set_volume(1)

DEATH_SFX = pygame.mixer.Sound(os.path.join("Assets/sounds", "die.wav"))
DEATH_SFX.set_volume(1)

COIN_SFX = pygame.mixer.Sound(os.path.join("Assets/sounds", "point.wav"))
COIN_SFX.set_volume(1)

BG_MUSIC_PATH = os.path.join("Assets/sounds", "western.mp3")
DEATH_MUSIC_PATH = os.path.join("Assets/sounds", "game_over.mp3")
MENU_MUSIC_PATH = os.path.join("Assets/sounds", "desert.mp3")
VICTORY_MUSIC_PATH = os.path.join("Assets/sounds", "Victory.mp3")

FONT_PATH = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
TITLE_IMAGE = pygame.image.load(os.path.join("Assets/Other", "Title.png"))
TITLE_IMAGE = pygame.transform.scale(TITLE_IMAGE, (900, 245 ))

LOADING_FRAMES = [
    pygame.image.load(f"Assets/Other/loading{i+1}.png").convert_alpha()
    for i in range(15)
]




class Dinosaur:
    X_POS = 80
    Y_POS = 335
    Y_POS_DUCK = 335
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.jump_sfx = JUMP_SFX

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
            self.jump_sfx.play()

        if userInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            self.jump_sfx.play()

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
        self.hitbox = pygame.Rect(self.dino_rect.x + 12, self.dino_rect.y + 30, 30, 40)
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.hitbox = pygame.Rect(self.dino_rect.x + 1, self.dino_rect.y + 9, 30, 40)
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.image:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 1

        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

        self.hitbox = pygame.Rect(self.dino_rect.x + 10, self.dino_rect.y + 13, 50, 50)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
       # pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = NOTE
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


        self.image = pygame.image.load(os.path.join("Assets/Background", "Bg.png"))


        self.image_width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.image_width
        self.y = 0

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


class Menu_Background:
    def __init__(self):

        self.bgmenu = MENU_BG
        self.image_width = self.bgmenu.get_width()
        self.x1 = 0
        self.x2 = self.image_width
        self.y = 5

    def update(self):
        pass

    def draw(self, SCREEN):
        SCREEN.blit(self.bgmenu, (self.x1, self.y))


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
        self.hitbox.y = self.rect.y + 10
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        #pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 350
        self.hitbox = pygame.Rect(self.rect.x + 5, self.rect.y + 10, self.rect.width - 10, self.rect.height - 10)


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 330
        self.hitbox = pygame.Rect(self.rect.x + 5, self.rect.y + 10, self.rect.width - 10, self.rect.height - 10)


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 300
        self.index = 0
        self.hitbox = pygame.Rect(self.rect.x + 10, self.rect.y + 35, 80, 50)

    def update(self):
        self.rect.x -= game_speed
        self.hitbox.x = self.rect.x + 10
        self.hitbox.y = self.rect.y + 10
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
       # pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)
        self.index += 1


class Coin:
    def __init__(self, obstacle):
        self.image = pygame.image.load(os.path.join("Assets/Background", "bulb.png"))
        self.rect = self.image.get_rect()
        self.rect.x = obstacle.rect.x + obstacle.rect.width // 2 - self.image.get_width() // 2

        if obstacle.rect.y == 280:
            self.rect.y = obstacle.rect.y + obstacle.rect.height + 50
        else:
            self.rect.y = obstacle.rect.y - self.image.get_height() - 50
        self.collected = False

    def update(self):
        self.rect.x -= game_speed

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

def loop_loading_animation(screen, duration_ms=3000, y_pos=600, message="", color=(255, 0, 0), bg_image=None):
    start_time = pygame.time.get_ticks()
    frame_index = 0
    frame_delay = 100

    font = pygame.font.Font(FONT_PATH, 50)
    text = font.render(message, True, color)
    text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
    text_y = SCREEN_HEIGHT // 3 - text.get_height() // 2

    while pygame.time.get_ticks() - start_time < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((255, 255, 255))

        screen.blit(text, (text_x, text_y))

        frame = LOADING_FRAMES[frame_index]
        frame_x = SCREEN_WIDTH // 2 - frame.get_width() // 2
        screen.blit(frame, (frame_x, y_pos))

        pygame.display.update()
        pygame.time.delay(frame_delay)
        frame_index = (frame_index + 1) % len(LOADING_FRAMES)


def pause_menu():
    paused = True
    font = pygame.font.Font(FONT_PATH, 30)
    title_font = pygame.font.Font(FONT_PATH, 50)
    selected_option = 0
    options = ["Play", "Restart", "How to Play"]

    while paused:
        SCREEN.blit(MENU_BG, (0, 0))  # background color

        # Title
        title_text = title_font.render("Game Paused", True, (255, 0, 0))
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Instructions
        if selected_option == 2:
            instructions = [
                "Press SPACE or UP arrow key to Jump",
                "Press DOWN arrow key to Duck",
                "Press ESC again to return"
            ]
            for i, line in enumerate(instructions):
                line_text = font.render(line, True, (0, 0, 0))
                SCREEN.blit(line_text, (SCREEN_WIDTH // 2 - line_text.get_width() // 2, 250 + i * 40))
        else:
            for i, option in enumerate(options):
                color = (0, 200, 0) if i == selected_option else (0, 0, 0)
                option_text = font.render(option, True, color)
                SCREEN.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 250 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Play
                        paused = False
                    elif selected_option == 1:  # Restart
                        mixer.music.stop()
                        main()  # restart game
                        return
                    elif selected_option == 2:  # How to Play
                        pass
                elif event.key == pygame.K_ESCAPE:
                    paused = False







def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    mixer.music.load(BG_MUSIC_PATH)
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

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

    coins = []
    collected_coins = 0
    next_coin_spawn_score = 300
    coins_spawned_for_score = False

    death_sfx = DEATH_SFX
    point_sfx = COIN_SFX

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        score_font = pygame.font.Font(FONT_PATH, 20)
        text = score_font.render("Score: " + str(points), True, (0, 0, 0))
        coin_text = score_font.render("Ideas: " + str(collected_coins) + "/5", True, (255, 215, 0))

        SCREEN.blit(coin_text, (1000, 70))
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
        if userInput[pygame.K_ESCAPE]:
            pause_menu()

        background_img.draw(SCREEN)
        background_img.update()
        background()

        cloud.draw(SCREEN)
        cloud.update()

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



        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.hitbox.colliderect(obstacle.hitbox):
                mixer.music.stop()
                death_sfx.play()
                mixer.music.load(DEATH_MUSIC_PATH)
                mixer.music.set_volume(0.5)
                mixer.music.play()
                # font = pygame.font.Font(FONT_PATH, 50)
                # game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
                # SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                #                              SCREEN_HEIGHT // 3 - game_over_text.get_height() // 3))

                pygame.display.update()
                loop_loading_animation(SCREEN, 5200, 250, "GAME OVER!", (255, 0, 0), bg_image=MENU_BG)


                pygame.time.delay(300)

                death_count += 1

                menu(death_count)

        if points >= next_coin_spawn_score and not coins_spawned_for_score:
            if obstacles:
                for _ in range(1):
                    obstacle = random.choice(obstacles)
                    coins.append(Coin(obstacle))
                coins_spawned_for_score = True

        active_coins = 0
        for coin in coins:
            coin.update()
            coin.draw(SCREEN)
            if not coin.collected and player.dino_rect.colliderect(coin.rect):
                point_sfx.play()
                coin.collected = True
                collected_coins += 1
            if not coin.collected and coin.rect.right > 0:
                active_coins += 1

        if collected_coins == 5:
            mixer.music.stop()
            mixer.music.load(VICTORY_MUSIC_PATH)
            mixer.music.set_volume(0.5)
            mixer.music.play()

            # font = pygame.font.Font(FONT_PATH, 50)
            # victory_text = font.render("VICTORY!", True, (0, 200, 0))
            # SCREEN.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2,
            #                            SCREEN_HEIGHT // 3 - victory_text.get_height() // 2))
            pygame.display.update()
            loop_loading_animation(SCREEN, 5500, 250, "VICTORY!", (0, 200, 0), bg_image=MENU_BG)
            pygame.time.delay(2000)

            pygame.quit()


        if coins_spawned_for_score and active_coins == 0:
            next_coin_spawn_score += 300
            coins_spawned_for_score = False
            coins.clear()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    mixer.music.load(MENU_MUSIC_PATH)
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    clock = pygame.time.Clock()
    step_index = 0

    menu_bg = Menu_Background()
    font = pygame.font.Font(FONT_PATH, 20)

    while run:
        SCREEN.fill((255, 255, 255))
        menu_bg.draw(SCREEN)

        title_rect = TITLE_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 190))
        SCREEN.blit(TITLE_IMAGE, title_rect)

        if death_count == 0:
            start_text = font.render("Press Enter to Start", True, (0, 0, 0))
        else:
            start_text = font.render("Press Enter to Restart", True, (0, 0, 0))
            score = font.render(f"Your Score: {points}", True, (255, 215, 0))
            SCREEN.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, SCREEN_HEIGHT // 2 + 165))

        exit_text = font.render("Press Esc to Exit", True, (0, 0, 0))
        desc_text = ("Objective: Collect 5 idea orbs while avoiding"
                     "\ndistractions and cliches that get in your way")

        SCREEN.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2+90))
        SCREEN.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 130))
        lines = desc_text.split('\n')
        for i, line in enumerate(lines):
            rendered_line = font.render(line, True, (0, 0, 0))
            SCREEN.blit(rendered_line, (SCREEN_WIDTH // 2 - rendered_line.get_width() // 2, 270 + i * 40))

        SCREEN.blit(RUNNING[step_index // 5], (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 10))
        step_index += 1
        if step_index >= 10:
            step_index = 0

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    mixer.music.stop()
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False

menu(death_count=0)
