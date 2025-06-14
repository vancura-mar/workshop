import random
from .game_object import GameObject

class Bee(GameObject):
    def __init__(self, screen_width, max_x=None, speed_y=4):
        width = 15
        height = 15
        # Pokud je max_x zadáno, včela se může spawnovat jen do této pozice
        if max_x is None:
            max_x = screen_width - width
        x = random.randint(0, max_x)
        y = -height  # Začíná těsně nad obrazovkou
        color = (255, 220, 50)  # Světle žlutá
        super().__init__(x, y, width, height, color, speed_y)

    # Pokud bude potřeba, lze přidat další logiku specifickou pro včelu 