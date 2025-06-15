import pygame
import time

class Player:
    def __init__(self, x, y, width=70, height=90, speed=5, screen_height=800):
        """Inicializace včelaře"""
        self.x = x
        # Y-ová pozice je vždy na spodní hraně
        self.y = screen_height - height
        self.width = width
        self.height = height
        self.speed = speed
        self.lives = 3  # počet životů
        self.score = 0
        self.rect = pygame.Rect(x, self.y, width, height)
        self.color = (255, 200, 0)  # Žlutá barva pro včelaře
        self.image = pygame.image.load("assets/beekeeper-scaled.png").convert_alpha()
        self.screen_height = screen_height
        self.stunned_until = 0  # čas do kdy je hráč omráčen
        self.bee_buffer = 0           # zásobník včel
        self.bee_buffer_max = 5       # maximální kapacita zásobníku
        self.sprite_frame_width = 123 // 2
        self.sprite_frame_height = 127 // 2

        self.animation_frames_walk = []
        self.animation_frame_idle = None
        self.current_frame_index = 0
        self.last_animation_update = pygame.time.get_ticks()
        self.animation_speed = 150  # Milisekundy na snímek animace

        self.is_moving = False
        self.facing_right = True  # defaultně kouká doprava

        if self.image:
            rect_walk_1 = pygame.Rect(0, 0, self.sprite_frame_width, self.sprite_frame_height)
            self.animation_frames_walk.append(self.image.subsurface(rect_walk_1))
            rect_walk_2 = pygame.Rect(self.sprite_frame_width, 0, self.sprite_frame_width, self.sprite_frame_height)
            self.animation_frames_walk.append(self.image.subsurface(rect_walk_2))

            rect_idle = pygame.Rect(0, self.sprite_frame_height, self.sprite_frame_width, self.sprite_frame_height)
            self.animation_frame_idle = self.image.subsurface(rect_idle)

            self.image = pygame.transform.scale(self.animation_frame_idle, (self.width, self.height))
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 200, 0))  # Původní žlutá barva

    def update_animation(self):
        """Aktualizuje snímek animace."""
        if not self.image:
            return

        now = pygame.time.get_ticks()

        if self.is_moving:
            if now - self.last_animation_update > self.animation_speed:
                self.last_animation_update = now
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames_walk)
                current_sprite_frame = self.animation_frames_walk[self.current_frame_index]
            else:
                current_sprite_frame = self.animation_frames_walk[self.current_frame_index]
        else:
            self.current_frame_index = 0
            current_sprite_frame = self.animation_frame_idle

        if not self.facing_right:
            current_sprite_frame = pygame.transform.flip(current_sprite_frame, True, False)

        self.image = pygame.transform.scale(current_sprite_frame, (self.width, self.height))


    def is_stunned(self):
        return time.time() < self.stunned_until

    def move(self, dx, screen_width, max_x=None):
        """Pohyb včelaře pouze doleva a doprava po spodní hraně obrazovky, s možností omezení maximální x-ové pozice (např. úl)."""
        if self.is_stunned():
            self.is_moving = False
            return  # pokud je omráčen, nemůže se hýbat

        if dx != 0:
            self.is_moving = True
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False
        else:
            self.is_moving = False

        new_x = self.x + dx * self.speed
        min_x = 0
        if max_x is None:
            max_x = screen_width - self.width
        new_x = max(min_x, min(new_x, max_x))
        self.x = new_x
        self.rect.x = self.x
        # Y-ová pozice je vždy na spodní hraně
        self.rect.y = self.screen_height - self.height

    def draw(self, screen):
        """Vykreslení včelaře"""
        self.update_animation()
        screen.blit(self.image, self.rect.topleft)
