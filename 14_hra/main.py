import pygame
import sys
import time
import math
from menu import Menu

# Inicializace
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bee Saver")
font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 20)
clock = pygame.time.Clock()

# Načtení loga
logo_img = pygame.image.load("assets/gameLogo.png")
logo_img = pygame.transform.scale(logo_img, (450, 420))

loading_bg = pygame.image.load("assets/loadingbackground.png")
loading_bg = pygame.transform.scale(loading_bg, (WIDTH, HEIGHT))

# Proměnné pro horizontální posun pozadí (scrollování)
cloud_offset = 0
# Proměnné pro animaci loga
logo_anim_time = 0
# Proměnné pro animaci teček v loading textu
loading_dots_time = 0
# Proměnné pro časovač loading screenu
loading_screen_time = 0

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 100, 255)

# Herní stavy
STATE_INTRO = "intro"
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_INSTRUCTIONS = "instructions"
STATE_TRANSITION = "transition"
state = STATE_INTRO

# Proměnné pro přechod
transition_alpha = 0
transition_speed = 2
transition_surface = pygame.Surface((WIDTH, HEIGHT))
transition_direction = 1

# Časovač úvodní obrazovky
intro_start_time = time.time()
INTRO_DURATION = 3

# Inicializace menu
menu = Menu(screen, WIDTH, HEIGHT)

def set_state(new_state):
    global state
    state = new_state

def exit_game():
    pygame.quit()
    sys.exit()

def draw_text_with_border(surface, text, font, center, text_color, border_color, border_width=2):
    text_surf = font.render(text, True, border_color)
    for dx in [-border_width, 0, border_width]:
        for dy in [-border_width, 0, border_width]:
            if dx != 0 or dy != 0:
                rect = text_surf.get_rect(center=(center[0] + dx, center[1] + dy))
                surface.blit(text_surf, rect)
    text_surf = font.render(text, True, text_color)
    rect = text_surf.get_rect(center=center)
    surface.blit(text_surf, rect)

def draw_intro():
    global cloud_offset, logo_anim_time, loading_dots_time, loading_screen_time
    cloud_offset += 0.7
    if cloud_offset > WIDTH:
        cloud_offset = 0
    screen.blit(loading_bg, (-cloud_offset, 0))
    screen.blit(loading_bg, (-cloud_offset + WIDTH, 0))
    
    logo_anim_time += 0.04
    hop_offset = math.sin(logo_anim_time) * 10
    logo_rect = logo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + hop_offset))
    screen.blit(logo_img, logo_rect)
    
    loading_dots_time += 1
    loading_screen_time += 1
    if loading_screen_time < 120:
        num_dots = (loading_dots_time // 20) % 4
        dots = "." * num_dots
        loading_text = small_font.render(f"LOADING GAME{dots}", True, (255, 255, 255))
    else:
        loading_text = small_font.render("STARTING...", True, (255, 255, 255))
    text_rect = loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 240))
    screen.blit(loading_text, text_rect)

def draw_transition():
    global transition_alpha, state, transition_direction
    if transition_direction == 1:
        draw_intro()
    else:
        menu.draw()
    
    transition_surface.fill((0, 0, 0))
    transition_surface.set_alpha(transition_alpha)
    screen.blit(transition_surface, (0, 0))
    
    transition_alpha += transition_speed * transition_direction
    
    if transition_alpha <= 0:
        transition_alpha = 0
        state = STATE_MENU
    elif transition_alpha >= 255:
        transition_alpha = 255
        transition_direction = -1

def draw_game():
    screen.fill(WHITE)
    text = font.render("Hra začala!", True, BLACK)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

def draw_instructions():
    screen.fill(WHITE)
    title = font.render("Návod", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    instructions = [
        "Pomocí šipek nebo WASD ovládej postavu.",
        "Cílem je nasbírat co nejvíc bodů.",
        "Kolize s překážkami tě poškodí.",
        "Zmáčkni ESC pro návrat do menu."
    ]

    for i, line in enumerate(instructions):
        line_surf = small_font.render(line, True, BLACK)
        screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, 150 + i * 40))

# Herní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_MENU and event.type == pygame.MOUSEBUTTONDOWN:
            clicked_button = menu.handle_click(event.pos)
            if clicked_button == "EXIT GAME":
                exit_game()
            elif clicked_button == "START GAME":
                set_state(STATE_GAME)
            elif clicked_button == "INSTRUCTIONS":
                set_state(STATE_INSTRUCTIONS)

        if state == STATE_INSTRUCTIONS and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_state(STATE_MENU)

        if state == STATE_GAME and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_state(STATE_MENU)

        if state == STATE_INTRO and event.type == pygame.KEYDOWN:
            set_state(STATE_TRANSITION)

    if state == STATE_INTRO:
        draw_intro()
        if loading_screen_time > 180:
            set_state(STATE_TRANSITION)
    elif state == STATE_TRANSITION:
        draw_transition()
    elif state == STATE_MENU:
        menu.draw()
    elif state == STATE_GAME:
        draw_game()
    elif state == STATE_INSTRUCTIONS:
        draw_instructions()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()