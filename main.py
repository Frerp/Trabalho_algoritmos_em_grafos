import pygame
import sys
import random
from characters.character import Character, Enemy
from gui.buttons import Button  # Adicionado import para a classe Button
from utils.graph_data import load_graph_data, load_coordinates_data
from events.events import handle_event, generate_random_event

pygame.init()

WIDTH, HEIGHT = 1200, 600
MENU_WIDTH = 400  # Largura do menu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ilha dos Perigos")

clock = pygame.time.Clock()

background_image = pygame.image.load('Assets/mapa_ilha10.jpeg')
background_image = pygame.transform.scale(background_image, (800, HEIGHT))

vertices_pos = load_coordinates_data("coordenadas_vertices.txt")
lista_adjacencias = load_graph_data("grafo.txt")

eventos_por_vertice = {i + 1: generate_random_event() for i in range(len(vertices_pos))}

initial_vertex = vertices_pos[0]
player = Character('Assets/frerp.png', initial_vertex, health=100, attack=20)
player.enemies = [Enemy('Pantera Mítica', health=50, attack=15),
                   Enemy('Leão de Nemeia', health=70, attack=20),
                   Enemy('Cobra Gigante', health=40, attack=25),
                   Enemy('Formigas Quimeras', health=60, attack=18)]

menu_surface = pygame.Surface((MENU_WIDTH, HEIGHT))
menu_surface.fill((50, 50, 50))

info_section = pygame.Surface((MENU_WIDTH, HEIGHT // 2))
info_bg_image = pygame.image.load('Assets/perga.jpg')
info_bg_image = pygame.transform.scale(info_bg_image, (MENU_WIDTH, HEIGHT // 2))
info_section.blit(info_bg_image, (0, 0))

events_section = pygame.Surface((MENU_WIDTH, HEIGHT // 2))
events_bg_image = pygame.image.load('Assets/perga.jpg')
events_bg_image = pygame.transform.scale(events_bg_image, (MENU_WIDTH, HEIGHT // 2))
events_section.blit(events_bg_image, (0, 0))

menu_surface.blit(info_section, (WIDTH - MENU_WIDTH, HEIGHT // 2))
menu_surface.blit(events_section, (WIDTH - MENU_WIDTH, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            current_vertex = player.current_vertex
            current_vertex_id = vertices_pos.index(current_vertex) + 1
            target_vertex = random.choice(lista_adjacencias[current_vertex_id])

            event_type = eventos_por_vertice.get(target_vertex, None)

            if event_type:
                event_description = handle_event(event_type)
                print(event_description)

                player.move_to_vertex(vertices_pos[target_vertex - 1])
                player.handle_event(event_type, screen)  # Adicionado o parâmetro screen

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(player.image, player.rect.topleft)

    font = pygame.font.Font(None, 26)
    health_text = font.render(f"Vida: {player.health}", True, (255, 255, 255))
    attack_text = font.render(f"Ataque: {player.attack}", True, (255, 255, 255))

    screen.blit(health_text, (920, 500))
    screen.blit(attack_text, (920, 530))
    player_icon = pygame.image.load('Assets/frerp.png')
    player_icon = pygame.transform.scale(player_icon, (190, 190))
    screen.blit(player_icon, (750, 440))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
