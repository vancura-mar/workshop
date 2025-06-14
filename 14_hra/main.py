import pygame
import sys
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moje hra")
font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 26)
clock = pygame.time.Clock()

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
state = STATE_INTRO
intro_start_time = time.time()
INTRO_DURATION = 3

def set_state(new_state):
    global state
    state = new_state

def exit_game():
    pygame.quit()
    sys.exit()

# Tlačítka v menu
menu_buttons = []
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60
BUTTON_SPACING = 20

def add_menu_button(text, callback):
    menu_buttons.append({
        "text": text,
        "callback": callback,
        "rect": pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    })

def layout_menu_buttons():
    total_height = len(menu_buttons) * BUTTON_HEIGHT + (len(menu_buttons) - 1) * BUTTON_SPACING
    start_y = HEIGHT // 2 - total_height // 2
    for i, button in enumerate(menu_buttons):
        x = WIDTH // 2 - BUTTON_WIDTH // 2
        y = start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING)
        button["rect"].topleft = (x, y)

def draw_button(button):
    pygame.draw.rect(screen, BLUE, button["rect"])
    text_surf = font.render(button["text"], True, WHITE)
    text_rect = text_surf.get_rect(center=button["rect"].center)
    screen.blit(text_surf, text_rect)

def handle_menu_click(pos):
    for button in menu_buttons:
        if button["rect"].collidepoint(pos):
            button["callback"]()

# Kreslení jednotlivých stavů
def draw_intro():
    screen.fill(BLACK)
    text = font.render("Vítej ve hře!", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

def draw_menu():
    screen.fill(GRAY)
    title = font.render("Menu", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    for button in menu_buttons:
        draw_button(button)

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

# Tlačítka
add_menu_button("Hrát", lambda: set_state(STATE_GAME))
add_menu_button("Návod", lambda: set_state(STATE_INSTRUCTIONS))
add_menu_button("Ukončit", exit_game)
layout_menu_buttons()

# Herní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_MENU and event.type == pygame.MOUSEBUTTONDOWN:
            handle_menu_click(event.pos)

        if state == STATE_INSTRUCTIONS and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_state(STATE_MENU)

    # Vykreslení aktuálního stavu
    if state == STATE_INTRO:
        draw_intro()
        if time.time() - intro_start_time > INTRO_DURATION:
            set_state(STATE_MENU)
    elif state == STATE_MENU:
        draw_menu()
    elif state == STATE_GAME:
        draw_game()
    elif state == STATE_INSTRUCTIONS:
        draw_instructions()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
