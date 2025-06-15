import random
import pygame
from .game_object import GameObject


class Wasp(GameObject):
    def __init__(self, screen_width, max_x=None, speed_y=5):

        width = 40
        height = 40
        # Pokud je max_x zadáno, vosa se může spawnovat jen do této pozice
        if max_x is None:
            max_x = screen_width - width
        x = random.randint(0, max_x)
        y = -height  # Začíná těsně nad obrazovkou
        color = (30, 30, 30)  # Tmavá barva pro vosu
        sprite_sheet = pygame.image.load("assets/zla-vosa.png").convert_alpha()
        frame_count = 4
        frame_width = sprite_sheet.get_width()
        frame_height = sprite_sheet.get_height() // frame_count
        self.frames = []
        for i in range(frame_count):
            frame = sprite_sheet.subsurface((0, i * frame_height, frame_width, frame_height))
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