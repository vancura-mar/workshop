import pygame
import sys
import math

# Konstanty pro menu
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_SPACING = 0

class Menu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.buttons = []
        self.cloud_offset = 0
        
        # Načtení fontů
        self.small_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 20)
        self.hover_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 22)
        
        # Načtení obrázků
        self.logo_img = pygame.image.load("assets/gameLogo.png")
        self.logo_img = pygame.transform.scale(self.logo_img, (450, 420))
        self.night_menu_bg = pygame.image.load("assets/nightMenu.png")
        self.night_menu_bg = pygame.transform.scale(self.night_menu_bg, (width, height))
        
        # Barvy
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 225, 74)
        
        # Inicializace tlačítek
        self.init_buttons()
    
    def init_buttons(self):
        menu_labels = ["START GAME", "INSTRUCTIONS", "CREDITS", "EXIT GAME"]
        self.buttons.clear()
        total_height = len(menu_labels) * BUTTON_HEIGHT + (len(menu_labels) - 1) * BUTTON_SPACING
        start_y = self.logo_img.get_rect(center=(self.width // 2, 80)).bottom + 10
        
        for i, label in enumerate(menu_labels):
            x = self.width // 2 - BUTTON_WIDTH // 2
            if i == 3:  # Poslední tlačítko
                y = start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING) + 18
            else:
                y = start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING)
            rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.buttons.append({
                "text": label,
                "rect": rect
            })
    
    def handle_click(self, pos):
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                return button["text"]
        return None
    
    def draw(self):
        # Animované pozadí menu
        self.cloud_offset += 0.4
        if self.cloud_offset > self.width:
            self.cloud_offset = 0
        self.screen.blit(self.night_menu_bg, (-self.cloud_offset, 0))
        self.screen.blit(self.night_menu_bg, (-self.cloud_offset + self.width, 0))
        
        # Fade/dýchání overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        t = pygame.time.get_ticks() / 1000
        alpha = int(60 + 60 * (1 + math.sin(t * 0.5)))
        overlay.fill((20, 20, 60, alpha))
        self.screen.blit(overlay, (0, 0))
        
        # Animace loga
        scale = 1.0 + 0.05 * math.sin(t * 0.8)
        angle = math.sin(t * 0.6) * 3
        logo_scaled = pygame.transform.rotozoom(self.logo_img, angle, scale)
        logo_rect = logo_scaled.get_rect(center=(self.width // 2, 150))
        self.screen.blit(logo_scaled, logo_rect)
        
        # Vykreslení tlačítek
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                color = self.YELLOW
                font_used = self.hover_font
            else:
                color = self.WHITE
                font_used = self.small_font
            
            text_surf = font_used.render(button["text"], True, color)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            self.screen.blit(text_surf, text_rect) 