import random
from .game_object import GameObject

class Honey(GameObject):
    def __init__(self, screen_width, max_x=None, speed_y=4):
        width = 20
        height = 20
        if max_x is None:
            max_x = screen_width - width
        x = random.randint(0, max_x)
        y = -height
        color = (255, 200, 40)  # Medová barva
        super().__init__(x, y, width, height, color, speed_y) 