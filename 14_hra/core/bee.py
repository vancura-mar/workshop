import random
import pygame
from .game_object import GameObject

class Bee(GameObject):
    def __init__(self, screen_width, max_x=None, speed_y=4):
        width = 40
        height = 40
        # Pokud je max_x zadáno, včela se může spawnovat jen do této pozice
        if max_x is None:
            max_x = screen_width - width
        x = random.randint(0, max_x)
        y = -height  # Začíná těsně nad obrazovkou
        color = (255, 220, 50)  # Světle žlutá

        sprite_sheet = pygame.image.load('assets/bees.png').convert_alpha()
        sprite_size = sprite_sheet.get_width() // 4
        bee_image = sprite_sheet.subsurface((0, 0, sprite_size, sprite_size))
        bee_image = pygame.transform.scale(bee_image, (width, height))
        super().__init__(x, y, width, height, color, speed_y, bee_image)

    # Pokud bude potřeba, lze přidat další logiku specifickou pro včelu 