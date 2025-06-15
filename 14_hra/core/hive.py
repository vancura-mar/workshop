import pygame
from .game_object import GameObject

class Hive(GameObject):
    def __init__(self, screen_width, screen_height, width=60, height=80):
        x = screen_width - width  # vpravo na obrazovce
        y = screen_height - height     # dole na obrazovce
        color = (180, 120, 40)         # hnědá barva
        self.original_image = pygame.image.load("assets/hive-scaled2.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        super().__init__(x, y, width, height, color, image=self.image)
        self.bee_buffer = 0            # zásobník včel v úlu
        self.bee_buffer_max = 15       # maximální kapacita úlu 