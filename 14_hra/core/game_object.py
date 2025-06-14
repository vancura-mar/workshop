import pygame

class GameObject:
    def __init__(self, x, y, width, height, color=(0, 0, 0), speed_y=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed_y = speed_y  # Rychlost pohybu ve směru y (např. padání)
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        """Aktualizace pozice objektu (např. padání)"""
        self.y += self.speed_y
        self.rect.y = self.y

    def draw(self, screen):
        """Vykreslení objektu"""
        pygame.draw.rect(screen, self.color, self.rect)

    def is_off_screen(self, screen_height):
        """Vrací True, pokud je objekt mimo spodní okraj obrazovky"""
        return self.y > screen_height 