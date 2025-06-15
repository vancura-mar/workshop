import pygame
import sys
from .player import Player
from .bee import Bee
from .hive import Hive
from .wasp import Wasp
from .honey import Honey
import random
import time

class Game:
    def __init__(self, width=500, height=700, title="Bee Saver"):
        """Inicializace hry"""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Vytvoření včelaře uprostřed dole
        self.player = Player(width//2 - 25, height, screen_height=height)
        
        # Vytvoření úlu vpravo dole
        self.hive = Hive(width, height)
        self.hive_forbidden_x = (self.hive.x, self.hive.x + self.hive.width)
        self.max_bee_x = self.hive.x - self.hive.width  # včela/vosa se může spawnovat jen do této pozice
        
        # Slovník pro sledování stisknutých kláves (pouze vlevo/vpravo)
        self.keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False
        }

        # Seznam včel
        self.bees = []
        self.spawn_timer = 0
        self.spawn_interval = 80  # Každých 80 ticků nová včela

        # Seznam vos
        self.wasps = []
        self.wasp_spawn_timer = 0
        self.wasp_spawn_interval = 160  # Každých 160 ticků nová vosa

        self.honey = None  # aktuální med (padá-li)

        # Načtení fontu
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 14)  # Malý font pro HUD
        self.large_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)  # Větší font pro Game Over info
        self.go_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 64)  # Velký font pro GAME OVER

        self.score = 0
        self.score_effect = None  # (text, x, y, time_end)
        self.life_effect = None   # (text, x, y, time_end)
        self.life_effect_end = 0  # čas do kdy zobrazovat efekt

        self.game_over = False
        
        # Načtení herního pozadí
        self.background = pygame.image.load("assets/gameBackground.png")
        self.background = pygame.transform.scale(self.background, (width, height))

        # Načtení ikonek srdíček pro životy
        HEART_SIZE = 48
        self.heart_icon = pygame.image.load("assets/heart-scaled.png").convert_alpha()
        self.heart_icon = pygame.transform.scale(self.heart_icon, (HEART_SIZE, HEART_SIZE))
        self.heart_off_icon = pygame.image.load("assets/heart-off-scaled.png").convert_alpha()
        self.heart_off_icon = pygame.transform.scale(self.heart_off_icon, (HEART_SIZE, HEART_SIZE))
        self.HEART_SIZE = HEART_SIZE
        self.HEART_SPACING = 2
        self.last_life_lost_time = 0
        self.last_life_lost_index = None
        self.prev_lives = self.player.lives

    def reset(self):
        self.player = Player(self.width//2 - 25, self.height, screen_height=self.height)
        self.hive = Hive(self.width, self.height)
        self.max_bee_x = self.hive.x - 15
        self.bees = []
        self.wasps = []
        self.honey = None
        self.spawn_timer = 0
        self.wasp_spawn_timer = 0
        self.score = 0
        self.score_effect = None
        self.life_effect_end = 0
        self.game_over = False
        self.running = True  
        self.keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False
        }
        self.prev_lives = self.player.lives

    def handle_events(self):
        """Zpracování událostí"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over and event.key == pygame.K_r:
                    self.reset()
                if self.game_over and event.key == pygame.K_RETURN:
                    self.running = False
                if event.key in self.keys and not self.game_over:
                    self.keys[event.key] = True
            if event.type == pygame.KEYUP:
                if event.key in self.keys:
                    self.keys[event.key] = False

    def update(self):
        """Aktualizace herního stavu"""
        if self.game_over:
            return
        dx = 0
        # Kontrola stisknutých kláves (pouze vlevo/vpravo)
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            dx -= 1
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            dx += 1
        # Maximální x-ová pozice je začátek úlu minus šířka včelaře
        max_x = self.hive.x - self.player.width
        self.player.move(dx, self.width, max_x=max_x)

        # Animace ztráty života
        if self.player.lives < self.prev_lives:
            self.last_life_lost_time = time.time()
            self.last_life_lost_index = self.player.lives
        self.prev_lives = self.player.lives

        # Detekce, že je včelař přímo u úlu (pravý okraj včelaře = levý okraj úlu)
        if self.player.rect.right == self.hive.rect.left:
            free_space = self.hive.bee_buffer_max - self.hive.bee_buffer
            bees_to_add = min(self.player.bee_buffer, free_space)
            self.hive.bee_buffer += bees_to_add
            self.player.bee_buffer -= bees_to_add
            self.score += bees_to_add  # zvýšení skóre
            if bees_to_add > 0:
                effect_x = self.hive.rect.centerx
                effect_y = self.hive.rect.top - 30
                self.score_effect = (f"+{bees_to_add}", effect_x, effect_y, time.time() + 0.7)

        # Spawnování včel
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.bees.append(Bee(self.width, max_x=self.max_bee_x))
            self.spawn_timer = 0

        # Spawnování vos
        self.wasp_spawn_timer += 1
        if self.wasp_spawn_timer >= self.wasp_spawn_interval:
            self.wasps.append(Wasp(self.width, max_x=self.max_bee_x))
            self.wasp_spawn_timer = 0

        # Aktualizace včel
        for bee in self.bees:
            bee.update()
        # Aktualizace vos
        for wasp in self.wasps:
            wasp.update()
        
        # Kontrola kolizí a odstranění včel, které narazily do včelaře
        new_bees = []
        for bee in self.bees:
            if bee.rect.colliderect(self.player.rect):
                if self.player.bee_buffer < self.player.bee_buffer_max:
                    self.player.bee_buffer += 1
                else:
                    new_bees.append(bee)
            else:
                new_bees.append(bee)
        # Pokud včela propadne dolů, odečíst život a zobrazit efekt
        self.bees = []
        for bee in new_bees:
            if bee.is_off_screen(self.height):
                self.player.lives -= 1
                self.life_effect_end = time.time() + 0.7
            else:
                self.bees.append(bee)

        # Kontrola kolizí vos s hráčem (odečtení životů)
        new_wasps = []
        for wasp in self.wasps:
            if wasp.rect.colliderect(self.player.rect):
                self.player.stunned_until = time.time() + 1  # 1 vteřina stun
            else:
                new_wasps.append(wasp)
        self.wasps = [wasp for wasp in new_wasps if not wasp.is_off_screen(self.height)]

        # Med jako odměna
        if self.hive.bee_buffer >= self.hive.bee_buffer_max and self.honey is None:
            self.honey = Honey(self.width, max_x=self.max_bee_x)
            self.hive.bee_buffer = 0  # vyresetovat úl

        # Pohyb a sbírání medu
        if self.honey:
            self.honey.update()
            # Kolize s hráčem
            if self.honey.rect.colliderect(self.player.rect):
                self.player.lives += 1
                self.honey = None
            # Propadnutí medu dolů
            elif self.honey.is_off_screen(self.height):
                self.honey = None

        if self.player.lives <= 0:
            self.game_over = True

    def draw(self):
        """Vykreslení herního stavu"""
        # Vykreslení pozadí místo bílého pozadí
        self.screen.blit(self.background, (0, 0))
        
        self.player.draw(self.screen)
        self.hive.draw(self.screen)
        for bee in self.bees:
            bee.draw(self.screen)
        for wasp in self.wasps:
            wasp.draw(self.screen)
        if self.honey:
            self.honey.draw(self.screen)
            
        # HUD - grafické čtverečky
        margin = 20
        section_spacing = 24  # větší mezera mezi sekcemi
        box_size = 18  # Zmenšené boxy pro lepší proporce
        spacing = 4    # Zmenšený spacing
        y = margin
        # PLAYER BEES
        text1 = self.font.render("PLAYER BEES:", True, (255,255,255))
        self.screen.blit(text1, (margin, y))
        y += text1.get_height() + 2
        for i in range(self.player.bee_buffer_max):
            color = (255, 200, 0) if i < self.player.bee_buffer else (220, 220, 220)
            pygame.draw.rect(self.screen, color, (margin + i*(box_size+spacing), y, box_size, box_size))
            pygame.draw.rect(self.screen, (0,0,0), (margin + i*(box_size+spacing), y, box_size, box_size), 2)
        self.screen.blit(self.font.render(f"/ {self.player.bee_buffer_max}", True, (255,255,255)), (margin + self.player.bee_buffer_max*(box_size+spacing) + 10, y))
        y += box_size + section_spacing  # větší mezera před další sekcí
        # HIVE BEES
        text2 = self.font.render("HIVE BEES:", True, (255,255,255))
        self.screen.blit(text2, (margin, y))
        y += text2.get_height() + 2
        for i in range(self.hive.bee_buffer_max):
            color = (255, 220, 50) if i < self.hive.bee_buffer else (220, 220, 220)
            pygame.draw.rect(self.screen, color, (margin + i*(box_size//1.5+spacing//1.5), y, int(box_size//1.5), int(box_size//1.5)))
            pygame.draw.rect(self.screen, (0,0,0), (margin + i*(box_size//1.5+spacing//1.5), y, int(box_size//1.5), int(box_size//1.5)), 2)
        self.screen.blit(self.font.render(f"/ {self.hive.bee_buffer_max}", True, (255,255,255)), (margin + int(self.hive.bee_buffer_max*(box_size//1.5+spacing//1.5)) + 10, y))
        y += int(box_size//1.5) + section_spacing  # větší mezera před další sekcí
        # LIVES
        text3 = self.font.render("LIVES:", True, (255,255,255))
        self.screen.blit(text3, (margin, y))
        y += text3.get_height() + 2
        for i in range(3):
            x = margin + i*(self.HEART_SIZE+self.HEART_SPACING)
            if i < self.player.lives:
                self.screen.blit(self.heart_icon, (x, y))
            else:
                if (self.last_life_lost_index == i and time.time() - self.last_life_lost_time < 0.3):
                    small_heart = pygame.transform.scale(self.heart_icon, (32, 32))
                    self.screen.blit(small_heart, (x + (self.HEART_SIZE-32)//2, y + (self.HEART_SIZE-32)//2))
                else:
                    self.screen.blit(self.heart_off_icon, (x, y))
        # Skóre
        y += box_size + margin//2
        score_text = self.font.render(f"SCORE: {self.score}", True, (255,255,255))
        score_rect = score_text.get_rect(topright=(self.width - margin, margin))
        self.screen.blit(score_text, score_rect)
        # Efekt získání bodů
        if self.score_effect:
            text, x, y, time_end = self.score_effect
            if time.time() < time_end:
                effect_surf = self.font.render(text, True, (0, 180, 0))
                rect = effect_surf.get_rect(center=(x, y))
                self.screen.blit(effect_surf, rect)
            else:
                self.score_effect = None
        # Efekt ztráty života (vždy nad aktuální pozicí hráče)
        if time.time() < self.life_effect_end:
            effect_x = self.player.rect.centerx
            effect_y = self.player.rect.top - 30
            effect_surf = self.font.render("-1", True, (200, 0, 0))
            rect = effect_surf.get_rect(center=(effect_x, effect_y))
            self.screen.blit(effect_surf, rect)
        # GAME OVER obrazovka
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            self.screen.blit(overlay, (0,0))
            go_text = self.go_font.render("GAME OVER", True, (255, 0, 0))
            go_rect = go_text.get_rect(center=(self.width//2, self.height//2 - 40))
            self.screen.blit(go_text, go_rect)
            score_text = self.large_font.render(f"SCORE: {self.score}", True, (255,255,255))
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2 + 30))
            self.screen.blit(score_text, score_rect)
            info_text = self.large_font.render("PRESS ESC TO EXIT", True, (255,255,255))
            info_rect = info_text.get_rect(center=(self.width//2, self.height//2 + 70))
            self.screen.blit(info_text, info_rect)
            restart_text = self.large_font.render("PRESS R TO RESTART", True, (255,255,0))
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 110))
            self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        return False  