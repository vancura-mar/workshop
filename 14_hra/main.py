import pygame
import sys
import time
import math
from menu import Menu
from core.game import Game

# Inicializace
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bee Saver")
font = pygame.font.SysFont("arial", 40)
clock = pygame.time.Clock()

# Herní stavy
STATE_INTRO = "intro"
STATE_MENU = "menu"
STATE_GAME = "game" 
STATE_INSTRUCTIONS = "instructions"
STATE_TRANSITION = "transition"
STATE_CREDITS = "credits"
state = STATE_INTRO

# Inicializace menu
menu = Menu(screen, WIDTH, HEIGHT)
game = Game(WIDTH, HEIGHT)

def set_state(new_state):
    global state
    state = new_state
    if new_state == STATE_GAME:
        game.reset()  

def exit_game():
    pygame.quit()
    sys.exit()

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
            elif clicked_button == "CREDITS":
                set_state(STATE_CREDITS)

        if state == STATE_INSTRUCTIONS and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_state(STATE_MENU)

        if state == STATE_GAME and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_state(STATE_MENU)

        if state == STATE_INTRO and event.type == pygame.KEYDOWN:
            set_state(STATE_TRANSITION)

        if state == STATE_CREDITS and event.type == pygame.MOUSEBUTTONDOWN:
            back_rect = menu.draw_credits()
            if back_rect.collidepoint(event.pos):
                set_state(STATE_MENU)
        if state == STATE_CREDITS and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_state(STATE_MENU)

        if state == STATE_INSTRUCTIONS and event.type == pygame.MOUSEBUTTONDOWN:
            back_rect = menu.draw_instructions()
            if back_rect.collidepoint(event.pos):
                set_state(STATE_MENU)

        if state == STATE_MENU and event.type == pygame.KEYDOWN:
            menu.keyboard_active = True
            if event.key == pygame.K_w:
                menu.selected_index = (menu.selected_index - 1) % len(menu.buttons)
            if event.key == pygame.K_s:
                menu.selected_index = (menu.selected_index + 1) % len(menu.buttons)
            if event.key == pygame.K_RETURN:
                selected = menu.buttons[menu.selected_index]["text"]
                if selected == "EXIT GAME":
                    exit_game()
                elif selected == "START GAME":
                    set_state(STATE_GAME)
                elif selected == "INSTRUCTIONS":
                    set_state(STATE_INSTRUCTIONS)
                elif selected == "CREDITS":
                    set_state(STATE_CREDITS)
        if state == STATE_MENU and event.type == pygame.MOUSEMOTION:
            if any(button["rect"].collidepoint(event.pos) for button in menu.buttons):
                menu.keyboard_active = False

    if state == STATE_INTRO:
        menu.draw_intro()
        if menu.loading_screen_time > 180:
            set_state(STATE_TRANSITION)
    elif state == STATE_TRANSITION:
        new_state = menu.draw_transition()
        if new_state != "transition":
            set_state(new_state)
    elif state == STATE_MENU:
        menu.draw()
    elif state == STATE_GAME:
        if not game.run():
            set_state(STATE_MENU)
    elif state == STATE_INSTRUCTIONS:
        menu.draw_instructions()
    elif state == STATE_CREDITS:
        menu.draw_credits()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()