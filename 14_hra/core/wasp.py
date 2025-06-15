import random
import pygame
from .game_object import GameObject


class Wasp(GameObject):
    def __init__(self, screen_width, max_x=None, speed_y=5):

        width = 15
        height = 15
        # Pokud je max_x zadáno, vosa se může spawnovat jen do této pozice
        if max_x is None:
            max_x = screen_width - width
        x = random.randint(0, max_x)
        y = -height  # Začíná těsně nad obrazovkou
        color = (30, 30, 30)  # Tmavá barva pro vosu
        sprite_sheet = pygame.image.load("assets/waspyboi-sprite.png").convert_alpha()
        sprite_width = sprite_sheet.get_width() // 2
        wasp_image = sprite_sheet.subsurface((0, 0, sprite_width, sprite_sheet.get_height()))
        self.image = pygame.transform.scale(wasp_image, (width, height))
        super().__init__(x, y, width, height, color, speed_y, self.image)