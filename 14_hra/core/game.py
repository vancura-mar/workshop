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
    def __init__(self, width=500, height=800, title="Bee Saver"):
        """Inicializace hry"""
        pygame.init()
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
        self.max_bee_x = self.hive.x - 15  # včela/vosa se může spawnovat jen do této pozice
        
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

        self.font = pygame.font.SysFont("arial", 28)

        self.score = 0
        self.score_effect = None  # (text, x, y, time_end)
        self.life_effect = None   # (text, x, y, time_end)
        self.life_effect_end = 0  # čas do kdy zobrazovat efekt

        self.game_over = False

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
        self.keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False
        }

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

        # Výpis počtu včel v zásobníku hráče a úlu
        print(f"Včely v zásobníku hráče: {self.player.bee_buffer} | Včely v úlu: {self.hive.bee_buffer} | Životy: {self.player.lives}")

        if self.player.lives <= 0:
            self.game_over = True

    def draw(self):
        """Vykreslení herního stavu"""
        self.screen.fill((255, 255, 255))
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
        box_size = 24
        spacing = 6
        y = margin
        # Včely u hráče
        text1 = self.font.render("Včely u hráče:", True, (0,0,0))
        self.screen.blit(text1, (margin, y))
        y += text1.get_height() + 2
        for i in range(self.player.bee_buffer_max):
            color = (255, 200, 0) if i < self.player.bee_buffer else (220, 220, 220)
            pygame.draw.rect(self.screen, color, (margin + i*(box_size+spacing), y, box_size, box_size))
            pygame.draw.rect(self.screen, (0,0,0), (margin + i*(box_size+spacing), y, box_size, box_size), 2)
        self.screen.blit(self.font.render(f"/ {self.player.bee_buffer_max}", True, (0,0,0)), (margin + self.player.bee_buffer_max*(box_size+spacing) + 10, y))
        y += box_size + margin//2
        # Včely v úlu
        text2 = self.font.render("Včely v úlu:", True, (0,0,0))
        self.screen.blit(text2, (margin, y))
        y += text2.get_height() + 2
        for i in range(self.hive.bee_buffer_max):
            color = (255, 220, 50) if i < self.hive.bee_buffer else (220, 220, 220)
            pygame.draw.rect(self.screen, color, (margin + i*(box_size//1.5+spacing//1.5), y, int(box_size//1.5), int(box_size//1.5)))
            pygame.draw.rect(self.screen, (0,0,0), (margin + i*(box_size//1.5+spacing//1.5), y, int(box_size//1.5), int(box_size//1.5)), 2)
        self.screen.blit(self.font.render(f"/ {self.hive.bee_buffer_max}", True, (0,0,0)), (margin + int(self.hive.bee_buffer_max*(box_size//1.5+spacing//1.5)) + 10, y))
        y += int(box_size//1.5) + margin//2
        # Životy
        text3 = self.font.render("Životy:", True, (0,0,0))
        self.screen.blit(text3, (margin, y))
        y += text3.get_height() + 2
        for i in range(3):
            color = (255, 80, 80) if i < self.player.lives else (220, 220, 220)
            pygame.draw.rect(self.screen, color, (margin + i*(box_size+spacing), y, box_size, box_size))
            pygame.draw.rect(self.screen, (0,0,0), (margin + i*(box_size+spacing), y, box_size, box_size), 2)
        self.screen.blit(self.font.render("/ 3", True, (0,0,0)), (margin + 3*(box_size+spacing) + 10, y))
        # Skóre
        y += box_size + margin//2
        text4 = self.font.render(f"Skóre: {self.score}", True, (0,0,0))
        self.screen.blit(text4, (margin, y))
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
            go_font = pygame.font.SysFont("arial", 64, bold=True)
            go_text = go_font.render("GAME OVER", True, (255, 0, 0))
            go_rect = go_text.get_rect(center=(self.width//2, self.height//2 - 40))
            self.screen.blit(go_text, go_rect)
            score_text = self.font.render(f"Skóre: {self.score}", True, (255,255,255))
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2 + 30))
            self.screen.blit(score_text, score_rect)
            info_text = self.font.render("Stiskni ESC pro ukončení", True, (255,255,255))
            info_rect = info_text.get_rect(center=(self.width//2, self.height//2 + 70))
            self.screen.blit(info_text, info_rect)
            restart_text = self.font.render("Stiskni R pro restart", True, (255,255,0))
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 110))
            self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    def run(self):
        """Hlavní herní smyčka"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit() 