import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#images
sun = pygame.image.load('img/sun.jpg')
bg = pygame.image.load('img/sky.jpg')

run = True


class world():
    def __init__(self, data):
        dirt = pygame.image.load('img/dirt.png')

        for row in data:
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt, (tile_size, tile_size))

world_data = [
[1, 1, 1, 1, 1],
[1, 0, 0, 0, 1],
[1, 0, 0, 0, 1],
[1, 0, 0, 0, 1],
[1, 1, 1, 1, 1],
]

while run == True:
    screen.blit(bg, (10, 0))
    screen.blit(sun, (200, 200))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
