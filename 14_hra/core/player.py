import pygame
import time

class Player:
    def __init__(self, x, y, width=50, height=50, speed=5, screen_height=800):
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
        self.screen_height = screen_height
        self.stunned_until = 0  # čas do kdy je hráč omráčen
        self.bee_buffer = 0           # zásobník včel
        self.bee_buffer_max = 5       # maximální kapacita zásobníku

    def is_stunned(self):
        return time.time() < self.stunned_until

    def move(self, dx, screen_width, max_x=None):
        """Pohyb včelaře pouze doleva a doprava po spodní hraně obrazovky, s možností omezení maximální x-ové pozice (např. úl)."""
        if self.is_stunned():
            return  # pokud je omráčen, nemůže se hýbat
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
        pygame.draw.rect(screen, self.color, self.rect) 