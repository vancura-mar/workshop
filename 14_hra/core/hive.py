import pygame
from .game_object import GameObject

class Hive(GameObject):
    def __init__(self, screen_width, screen_height, width=50, height=60):
        x = screen_width - width  # vpravo na obrazovce
        y = screen_height - height     # dole na obrazovce
        color = (180, 120, 40)         # hnědá barva
        super().__init__(x, y, width, height, color)
        self.bee_buffer = 0            # zásobník včel v úlu
        self.bee_buffer_max = 15       # maximální kapacita úlu 