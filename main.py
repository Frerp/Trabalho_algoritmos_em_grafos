import pygame
import sys
import random
from characters.character import Character, Enemy
from gui.buttons import Button  # Adicionado import para a classe Button
from utils.graph_data import load_graph_data, load_coordinates_data
from events.events import handle_event, generate_random_event
from events.generate_path import generate_path

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
#print("vertices_pos: ", vertices_pos)

index_initial_vertex, caminho_gerado = generate_path(lista_adjacencias)
#print("index_initial_vertex: ", index_initial_vertex)
#print("Caminho gerado: ", caminho_gerado)

eventos_por_vertice = {i + 1: generate_random_event() for i in range(len(vertices_pos))}

initial_vertex = vertices_pos[index_initial_vertex - 1]
player = Character('Assets/frerp.png', initial_vertex, health=100, attack=20)
player.enemies = [   Enemy('Pantera Mítica', health=50, attack=15, image_path='Assets/pantera.jpeg'),
                     Enemy('Leão de Nemeia', health=70, attack=20, image_path='Assets/leao.jpeg'),
                     Enemy('Cobra Gigante', health=40, attack=25, image_path='Assets/cobra.jpeg'),
                     Enemy('Formigas Quimeras', health=60, attack=18,image_path='Assets/formiga.jpeg')]

menu_surface = pygame.Surface((MENU_WIDTH, HEIGHT))
menu_surface.fill((50, 50, 50))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO
            current_vertex = player.current_vertex
            current_vertex_id_vertices_pos = vertices_pos.index(current_vertex) + 1

            current_vertex_id_caminho_gerado = caminho_gerado.index(current_vertex_id_vertices_pos)
            target_vertex_id_caminho_gerado = current_vertex_id_caminho_gerado + 1
            target_vertex = caminho_gerado[target_vertex_id_caminho_gerado]
            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO

            event_type = eventos_por_vertice.get(target_vertex, None)

            if event_type:
                event_description = handle_event(event_type)
                print(event_description)


                if 'inimigo' in event_type:
                    player.handle_event(event_type, screen)
                    player.move_to_vertex(vertices_pos[target_vertex - 1])
                elif 'cura' in event_type or 'arma' in event_type:
                    player.handle_event(event_type, screen)
                    player.move_to_vertex(vertices_pos[target_vertex - 1])
                elif 'deslizamento_pedra' in event_type or 'areia_movedica' in event_type or 'rio_traicoeiro' in event_type:
                    damage = random.randint(1, 10)
                    print(f"Você sofreu {damage} de dano devido ao evento.")
                    player.take_damage(damage)
                    print(f"Sua vida atual: {player.health}")
                    player.move_to_vertex(vertices_pos[target_vertex - 1])


    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(player.image, player.rect.topleft)


    #PRINTANDO GRAFO NA TELA PARA AJUDAR VISUALIZAÇÃO
    for vertice, adjacentes in lista_adjacencias.items():
        for adjacente in adjacentes:
            pygame.draw.line(screen, (0, 0, 255), vertices_pos[vertice - 1], vertices_pos[adjacente - 1], 2)
    
    fonte = pygame.font.Font(None, 26)
    for coordenada in vertices_pos:
        indice_vertice = fonte.render(f"{vertices_pos.index(coordenada) + 1}", True, (255, 255, 255))
        pygame.draw.circle(screen, (0, 0, 255), coordenada, 10)
        screen.blit(indice_vertice, (coordenada[0] + 10, coordenada[1] - 5))

    tamanho_caminho = len(caminho_gerado)
    for index in range(tamanho_caminho - 1):
        x = caminho_gerado[index]
        y = caminho_gerado[index + 1]
        pygame.draw.line(screen, (0, 255, 0), vertices_pos[x - 1], vertices_pos[y - 1], 2)
        pygame.draw.circle(screen, (0, 255, 0), vertices_pos[x - 1], 10)
        pygame.draw.circle(screen, (0, 255, 0), vertices_pos[y - 1], 10)
    #PRINTANDO GRAFO NA TELA PARA AJUDAR VISUALIZAÇÃO    


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