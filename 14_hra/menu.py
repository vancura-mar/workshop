import pygame
import sys
import math
import time

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
        self.selected_index = 0  # Nový atribut pro klávesové ovládání
        self.keyboard_active = True  # Nový atribut
        
        # Načtení fontů
        self.small_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 20)
        self.hover_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 22)
        
        # Načtení obrázků
        self.logo_img = pygame.image.load("assets/gameLogo.png")
        self.logo_img = pygame.transform.scale(self.logo_img, (450, 420))
        self.night_menu_bg = pygame.image.load("assets/nightMenu.png")
        self.night_menu_bg = pygame.transform.scale(self.night_menu_bg, (width, height))
        self.loading_bg = pygame.image.load("assets/loadingbackground.png")
        self.loading_bg = pygame.transform.scale(self.loading_bg, (width, height))
        
        # Barvy
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 225, 74)
        
        # Proměnné pro animace
        self.logo_anim_time = 0
        self.loading_dots_time = 0
        self.loading_screen_time = 0
        self.transition_alpha = 0
        self.transition_speed = 2
        self.transition_surface = pygame.Surface((width, height))
        self.transition_direction = 1
        
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
        for i, button in enumerate(self.buttons):
            is_hover = button["rect"].collidepoint(mouse_pos)
            is_selected = (i == self.selected_index and self.keyboard_active)
            if is_hover or is_selected:
                color = self.YELLOW
                font_used = self.hover_font
            else:
                color = self.WHITE
                font_used = self.small_font
            
            text_surf = font_used.render(button["text"], True, color)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            self.screen.blit(text_surf, text_rect)

    def draw_intro(self):
        self.cloud_offset += 0.7
        if self.cloud_offset > self.width:
            self.cloud_offset = 0
        self.screen.blit(self.loading_bg, (-self.cloud_offset, 0))
        self.screen.blit(self.loading_bg, (-self.cloud_offset + self.width, 0))
        
        self.logo_anim_time += 0.04
        hop_offset = math.sin(self.logo_anim_time) * 10
        logo_rect = self.logo_img.get_rect(center=(self.width // 2, self.height // 2 + hop_offset))
        self.screen.blit(self.logo_img, logo_rect)
        
        self.loading_dots_time += 1
        self.loading_screen_time += 1
        if self.loading_screen_time < 120:
            num_dots = (self.loading_dots_time // 20) % 4
            dots = "." * num_dots
            loading_text = self.small_font.render(f"LOADING GAME{dots}", True, (255, 255, 255))
        else:
            loading_text = self.small_font.render("STARTING...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(self.width // 2, self.height // 2 + 240))
        self.screen.blit(loading_text, text_rect)

    def draw_transition(self):
        if self.transition_direction == 1:
            self.draw_intro()
        else:
            self.draw()
        
        self.transition_surface.fill((0, 0, 0))
        self.transition_surface.set_alpha(self.transition_alpha)
        self.screen.blit(self.transition_surface, (0, 0))
        
        self.transition_alpha += self.transition_speed * self.transition_direction
        
        if self.transition_alpha <= 0:
            self.transition_alpha = 0
            return "menu"
        elif self.transition_alpha >= 255:
            self.transition_alpha = 255
            self.transition_direction = -1
        return "transition"

    def draw_instructions(self):
        # Stejné pozadí jako menu (včetně animace)
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
        
        # Větší font pro INSTRUCTIONS
        large_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 28)
        title = large_font.render("INSTRUCTIONS", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.width//2, 150))
        self.screen.blit(title, title_rect)
        
        # GOAL nadpis
        goal_title = self.small_font.render("GOAL", True, self.YELLOW)
        goal_rect = goal_title.get_rect(center=(self.width//2, 200))
        self.screen.blit(goal_title, goal_rect)
        
        # Instrukce GOAL
        instructions = [
            "Save the bees and bring them",
            "to the hive.",
            "Watch out for wasps, they'll stun you!",
            "Collect honey for extra lives."
        ]
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.width//2, 250 + i*36))
            self.screen.blit(text, text_rect)
        
        # MOVEMENT nadpis
        movement_title = self.small_font.render("MOVEMENT/CONTROLS", True, self.YELLOW)
        movement_rect = movement_title.get_rect(center=(self.width//2, 250 + len(instructions)*36 + 36))
        self.screen.blit(movement_title, movement_rect)
        
        # MOVEMENT instrukce
        movement_instruction = "Left/right arrows or A/D keys."
        movement_text = self.small_font.render(movement_instruction, True, self.WHITE)
        movement_text_rect = movement_text.get_rect(center=(self.width//2, 250 + len(instructions)*36 + 36 + 36))
        self.screen.blit(movement_text, movement_text_rect)
        
        # BACK vlevo nahoře ve stylu menu
        mouse_pos = pygame.mouse.get_pos()
        back_rect = pygame.Rect(20, 20, 100, 30)
        if back_rect.collidepoint(mouse_pos):
            back = self.small_font.render("< BACK", True, self.WHITE)
        else:
            back = self.small_font.render("< BACK", True, self.YELLOW)
        self.screen.blit(back, (20, 20))
        return back_rect

    def draw_credits(self):
        # Stejné pozadí jako menu (včetně animace)
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
        
        # Logo nahoře (menší)
        logo_scaled = pygame.transform.rotozoom(self.logo_img, 0, 0.6)
        logo_rect = logo_scaled.get_rect(center=(self.width // 2, 110))
        self.screen.blit(logo_scaled, logo_rect)
        
        # Nadpis
        title = self.small_font.render("CREDITS", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.width//2, 220))
        self.screen.blit(title, title_rect)
        
        # Game Design sekce
        section = self.small_font.render("Game Design & Development:", True, self.WHITE)
        section_rect = section.get_rect(center=(self.width//2, 270))
        self.screen.blit(section, section_rect)
        
        # Jména
        names = [
            "Adam Maleček (7743-6952-1)",
            "Martin Vančura (9890-1312-1)",
            "Lukáš Mužík (3965-9375-1)",
            "Dominik Vaňkát (6425-8941-1)"
        ]
        for i, name in enumerate(names):
            n = self.small_font.render(name, True, self.WHITE)
            n_rect = n.get_rect(center=(self.width//2, 320 + i*36))
            self.screen.blit(n, n_rect)
        
        # Made with
        made = self.small_font.render("Made with:", True, self.WHITE)
        made_rect = made.get_rect(center=(self.width//2, 500))
        self.screen.blit(made, made_rect)
        lib = self.small_font.render("Pygame", True, self.WHITE)
        lib_rect = lib.get_rect(center=(self.width//2, 540))
        self.screen.blit(lib, lib_rect)
        
        # BACK vlevo nahoře ve stylu menu
        mouse_pos = pygame.mouse.get_pos()
        back_rect = pygame.Rect(20, 20, 100, 30)
        if back_rect.collidepoint(mouse_pos):
            back = self.small_font.render("< BACK", True, self.WHITE)
        else:
            back = self.small_font.render("< BACK", True, self.YELLOW)
        self.screen.blit(back, (20, 20))
        return back_rect 