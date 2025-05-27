import pygame
import os
import random
pygame.init()

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
    Coins = coins()