import random
import pygame
from .game_object import GameObject

class Honey(GameObject):
    def __init__(self, screen_width, max_x=None, speed_y=4):
        width = 20
        height = 20
        if max_x is None:
            max_x = screen_width - width
        x = random.randint(0, max_x)
        y = -height
        self.original_image = pygame.image.load("assets/honeycomb.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        super().__init__(x, y, width, height, None, speed_y, image=self.image)