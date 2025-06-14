import pygame
import sys
import time

# Inicializace
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moje hra")
font = pygame.font.SysFont("arial", 40)

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 100, 255)

# Stav hry
STATE_INTRO = "intro"
STATE_MENU = "menu"
STATE_GAME = "game"
state = STATE_INTRO

# Časovač úvodní obrazovky
intro_start_time = time.time()
INTRO_DURATION = 3  # sekundy

# Tlačítko
button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)

def draw_intro():
    screen.fill(BLACK)
    text = font.render("Vítej ve hře!", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

def draw_menu():
    screen.fill(GRAY)
    title = font.render("Menu", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

    pygame.draw.rect(screen, BLUE, button_rect)
    button_text = font.render("Hrát", True, WHITE)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width()//2,
                              button_rect.centery - button_text.get_height()//2))

def draw_game():
    screen.fill(WHITE)
    text = font.render("Hra začala!", True, BLACK)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

# Herní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_MENU and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                state = STATE_GAME

    if state == STATE_INTRO:
        draw_intro()
        if time.time() - intro_start_time > INTRO_DURATION:
            state = STATE_MENU
    elif state == STATE_MENU:
        draw_menu()
    elif state == STATE_GAME:
        draw_game()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
