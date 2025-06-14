import pygame

class GameObject:
    def __init__(self, x, y, width, height, color=(0, 0, 0), speed_y=0, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed_y = speed_y
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image 

    def update(self):
        """Aktualizace pozice objektu (např. padání)"""
        self.y += self.speed_y
        self.rect.y = self.y

    def draw(self, screen):
        """Vykreslení objektu"""
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def is_off_screen(self, screen_height):
        """Vrací True, pokud je objekt mimo spodní okraj obrazovky"""
        return self.y > screen_height 