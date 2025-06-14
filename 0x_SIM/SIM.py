import pygame
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# nastavení matplotlib pro použití s Pygame
matplotlib.use("Agg")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600
FPS = 45

INDIVIDUAL_COUNT = 1000
TRANSMISSION_PROBABILITY = 0.1
INDIVIDUAL_SIZE = 10
RECOVERY_TIME = FPS * 10  # Předpokládejme, že se jedinci uzdraví po 10 sekundách (při 45 FPS)
DEATH_PROBABILITY = 0.005
CHANGE_DIR_PROBABILIY = 0.05


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infection Simulation")
clock = pygame.time.Clock()

class Individual(pygame.sprite.Sprite):
    def __init__(self, infected=False):
        super(Individual, self).__init__()
        self.image = pygame.Surface((INDIVIDUAL_SIZE, INDIVIDUAL_SIZE))
        self.infected = infected
        self.was_infected = infected
        self.infection_timer = RECOVERY_TIME if infected else 0  # Nastaví časovač pouze pro nakažené jedince
        self.image.fill(RED if self.infected else GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speedx = random.choice([-1, 0, 1])
        self.speedy = random.choice([-1, 0, 1])
        self.is_alive = True

    def infect(self):
        if not self.infected and self.is_alive:
            self.infected = True
            self.infection_timer = RECOVERY_TIME  # Resetuj časovač když je jedinec nakažený
            self.was_infected = True
            self.image.fill(RED)

    def recover(self):
        self.infected = False
        self.image.fill(GREEN)

    def update(self):
        if not self.is_alive: 
            return 
        if CHANGE_DIR_PROBABILIY > random.random():
            self.speedx = random.choice([-1, 0, 1])
            self.speedy = random.choice([-1, 0, 1])
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speedy = -self.speedy

        if self.infected:
            self.infection_timer -= 1
            if self.infection_timer <= 0:
                self.recover()

        if self.infected and self.is_alive:
            if random.random() < DEATH_PROBABILITY:
                self.die()

    def try_to_infect(self, others):
        if self.infected and self.is_alive:
            for other in others:
                # kontroluje, zda jiný jedinec není nakažený a zda předtím nebyl nakažený (tedy nemá imunitu)
                if other != self and not other.infected and not other.was_infected and self.rect.colliderect(other.rect):
                    if random.random() < TRANSMISSION_PROBABILITY:
                        other.infect()

    def die(self):
        self.is_alive = False
        self.infected = False
        self.image.fill((128, 128, 128))

def draw_graph(cumulative_infected, total_population):
    cumulative_percentage = [(x / total_population) * 100 for x in cumulative_infected]

    plt.figure(figsize=(2, 1.5))
    plt.plot(cumulative_percentage, color='purple')
    plt.xlabel('Time')
    plt.ylabel('Infected')
    plt.ylim(0, 100)
    plt.tight_layout()

    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(plt.gcf())
    canvas.draw()

    buf = canvas.buffer_rgba()  # získá surová RGBA data
    size = canvas.get_width_height()  # (šířka, výška)
    surf = pygame.image.frombuffer(buf, size, "RGBA")  # vytvoří Pygame Surface

    plt.close()

    return surf

def draw_bar_graph(current_infected, healthy_count, current_death, never_infected):
    indices = np.arange(4)
    values = [current_infected, healthy_count, current_death, never_infected]

    plt.figure(figsize=(2.5, 1.5)) 
    plt.bar(indices, values, color=['red', 'green', 'black','purple'], width = 0.4)
    plt.xticks(indices, [f'Infected \n {current_infected}', f'Healthy \n {healthy_count}', f'deathy\n{current_death}',f'nev.inf.\n{never_infected}'],fontsize= 7)
    plt.ylabel('No. of Ind.')
    plt.tight_layout()

    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(plt.gcf())
    canvas.draw()


    buf = canvas.buffer_rgba()  # získá surová RGBA data
    size = canvas.get_width_height()  # (šířka, výška)
    surf = pygame.image.frombuffer(buf, size, "RGBA")  # vytvoří Pygame Surface

    plt.close()


    return surf


def draw_line_graph(current_infected_list, healthy_list,death_list):
    plt.figure(figsize=(2.3, 1.7))
    plt.plot(current_infected_list, label='Currently Infected', color='red')
    plt.plot(healthy_list, label='Currently Healthy', color='green')
    plt.plot(death_list, label='N. deaths', color='black')
    plt.xlabel('Time')
    plt.ylabel('N. of ind.')
    plt.tight_layout()

    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(plt.gcf())
    canvas.draw()

    buf = canvas.buffer_rgba()  # získá surová RGBA data
    size = canvas.get_width_height()  # (šířka, výška)
    surf = pygame.image.frombuffer(buf, size, "RGBA")  # vytvoří Pygame Surface

    plt.close()

    return surf





population = pygame.sprite.Group()
initial_infected = random.sample([i for i in range(INDIVIDUAL_COUNT)], k=int(1))
for i in range(INDIVIDUAL_COUNT):
    individual = Individual(infected=(i in initial_infected))
    population.add(individual)

cumulative_infected = [len(initial_infected)]

current_infected_list = []
healthy_list = []
death_list = [0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    population.update()
    
    
    for individual in population:
        individual.try_to_infect(population)

    # stats
    current_infected = sum(1 for individual in population if individual.infected)
    cumulative_infected.append(sum(1 for individual in population if individual.was_infected or not individual.is_alive))
    never_infected = sum((1 for individual in population if not individual.was_infected))
    death_list.append(sum(1 for individual in population if not individual.is_alive))
    current_death = death_list[-1]
    healthy_count = INDIVIDUAL_COUNT - current_infected - current_death

    current_infected_list.append(current_infected)
    healthy_list.append(healthy_count)

    # Draw everything
    screen.fill(BLACK)
    population.draw(screen)
    graph_surf = draw_graph(cumulative_infected, INDIVIDUAL_COUNT)
    #Můžete nastavit pozici grafu, kam chcete
    graph_pos_x = WIDTH - graph_surf.get_width() 
    graph_pos_y = HEIGHT - graph_surf.get_height() 
    bar_graph_surf = draw_bar_graph(current_infected, healthy_count, current_death,never_infected)
    bar_graph_x = 0 
    bar_graph_y = HEIGHT - bar_graph_surf.get_height() 

    #...a přidáte toto volání do vaší smyčky pro aktualizaci a vykreslení grafů na obrazovku
    line_graph_surf = draw_line_graph(current_infected_list, healthy_list, death_list)
    line_graph_x = 0
    line_graph_y = 0
    screen.blit(line_graph_surf, (line_graph_x, line_graph_y))
    
    screen.blit(graph_surf, (graph_pos_x, graph_pos_y))
    screen.blit(bar_graph_surf, (bar_graph_x, bar_graph_y))

    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
