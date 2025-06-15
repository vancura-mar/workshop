import random
import pygame
from .game_object import GameObject

class Bee(GameObject):
    def __init__(self, screen_width, max_x=None, speed_y=4):
        width = 40
        height = 40
        if max_x is None:
            max_x = screen_width - width
        x = random.randint(0, max_x)
        y = -height  # Začíná těsně nad obrazovkou
        color = (255, 220, 50)  # Světle žlutá

        # Načtení sprite sheetu s animací včelky
        sprite_sheet = pygame.image.load('assets/bee-sprite.png').convert_alpha()
        frame_count = 4
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()
        bee_real_height = 384
        y_offset = (frame_height - bee_real_height) // 2
        self.frames = []
        for i in [2, 3]:
            frame = sprite_sheet.subsurface((i * frame_width, y_offset, frame_width, bee_real_height))
            frame = pygame.transform.scale(frame, (width, height))
            self.frames.append(frame)


        self.current_frame = 0
        self.animation_speed = 0.15  # sekundy na snímek
        self.last_update = pygame.time.get_ticks()

        super().__init__(x, y, width, height, color, speed_y, self.frames[0])

    def update(self):
        super().update()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]