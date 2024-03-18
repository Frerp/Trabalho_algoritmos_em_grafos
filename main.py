import pygame
import sys
import random
from characters.character import Character, Enemy
from gui.buttons import Button  # Adicionado import para a classe Button
from utils.graph_data import load_graph_data, load_coordinates_data
from events.events import handle_event, generate_random_event
from events.generate_path import generate_path
from determina_prox_vertice import determina_proximo_vertice

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


#DECLARAÇÃO DE VÉRTICE DE INÍCIO E DE DESTINO E CHECKPOINTS
vertices_inicio = [1, 2, 7]
index_vertice_inicial = random.choice(vertices_inicio)

vertices_tesouro = [20, 33, 34, 40, 42, 43, 44, 45, 46, 47, 48]
index_vertice_destino = random.choice(vertices_tesouro)

vertices_checkpoints = [19, 28, 36]
#DECLARAÇÃO DE VÉRTICE DE INÍCIO E DE DESTINO E CHECKPOINTS


#INICIALIZANOD PILHA E CAMINHO GERADO COM BUSCA EM LARGURA
pilha = []
caminho_gerado = generate_path(lista_adjacencias, index_vertice_inicial, index_vertice_destino)
#INICIALIZANOD PILHA E CAMINHO GERADO COM BUSCA EM LARGURA


#INICIALIZANDO PROGRESSO DO JOGO
progresso = []
#INICIALIZANDO PROGRESSO DO JOG

eventos_por_vertice = {}
for i in range(len(vertices_pos)):
    if (i + 1) not in vertices_checkpoints:
        eventos_por_vertice[i + 1] = generate_random_event()
    else:
        eventos_por_vertice[i + 1] = 'checkpoint'

vertice_inicial = vertices_pos[index_vertice_inicial  - 1]
player = Character('Assets/frerp.png', vertice_inicial, health=100, attack=20)
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


            #DETERMINA ID DO VÉRTICE ATUAL
            vertice_atual = player.current_vertex
            id_vertice_atual = vertices_pos.index(vertice_atual) + 1
            #DETERMINA ID DO VÉRTICE ATUAL


            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO (USANDO FUNÇÃO DETERMINA_PROXIMO_VERTICE)
            print("\nCABEÇALHO............................................")
            print("vertice atual: ", id_vertice_atual)
            print("cor vertice atual: ", lista_adjacencias[id_vertice_atual][0])
            print("qtd visitados vertice atual: ", lista_adjacencias[id_vertice_atual][1])
            print("lista de vizinhos vertice atual: ", lista_adjacencias[id_vertice_atual][2])
            lista_adjacencias, proximo_vertice, pilha = determina_proximo_vertice(lista_adjacencias, id_vertice_atual, pilha)
            target_vertex = proximo_vertice
            print("vertice atual (atualização): ", id_vertice_atual)
            print("cor vertice atual (atualização): ", lista_adjacencias[id_vertice_atual][0])
            print("qtd visitados vertice atual (atualização): ", lista_adjacencias[id_vertice_atual][1])
            print("lista de vizinhos vertice atual (atualização): ", lista_adjacencias[id_vertice_atual][2])
            print("proximo vertice: ", target_vertex)
            print("pilha: ", pilha)
            if (target_vertex == -1):
                running = False
            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO (USANDO FUNÇÃO DETERMINA_PROXIMO_VERTICE)

            #LIDANDO COM EVENTO DO VÉRTICE ATUAL
            event_type = eventos_por_vertice.get(id_vertice_atual, None)

            if event_type:
                event_description = (event_type)
                print(event_description)


                if 'inimigo' in event_type:
                    #player.handle_event(event_type, screen)
                    pass
                elif 'cura' in event_type or 'arma' in event_type:
                    #player.handle_event(event_type, screen)
                    pass
                elif 'deslizamento_pedra' in event_type or 'areia_movedica' in event_type or 'rio_traicoeiro' in event_type:
                    damage = random.randint(1, 10)
                    print(f"Você sofreu {damage} de dano devido ao evento.")
                    player.take_damage(damage)
                    print(f"Sua vida atual: {player.health}")
                    
                elif 'checkpoint' in event_type:
                    ultimo_checkpoint = id_vertice_atual
                    progresso = pilha
                    eventos_por_vertice[id_vertice_atual] = None
                    player.handle_event(event_type, screen)

            player.move_to_vertex(vertices_pos[target_vertex - 1])
            
            #DEPOIS QUE ELE PERDER VIDA, ELE VERIFICA SE USA CHECKPOINT
            #LIDANDO COM EVENTO DO VÉRTICE ATUAL


            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO (USANDO FUNÇÃO GENERATE_PATH)
            '''current_vertex = player.current_vertex
            current_vertex_id_vertices_pos = vertices_pos.index(current_vertex) + 1

            current_vertex_id_caminho_gerado = caminho_gerado.index(current_vertex_id_vertices_pos)
            target_vertex_id_caminho_gerado = current_vertex_id_caminho_gerado + 1
            target_vertex = caminho_gerado[target_vertex_id_caminho_gerado]'''
            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO (USANDO FUNÇÃO GENERATE_PATH)


    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(player.image, player.rect.topleft)


    #PRINTANDO GRAFO NA TELA PARA AJUDAR VISUALIZAÇÃO
    for vertice, vizinhanca in lista_adjacencias.items():
        for adjacente in vizinhanca[2]:
            pygame.draw.line(screen, (0, 0, 255), vertices_pos[vertice - 1], vertices_pos[adjacente - 1], 2)
    
    fonte = pygame.font.Font(None, 26)
    for coordenada in vertices_pos:
        indice_vertice = fonte.render(f"{vertices_pos.index(coordenada) + 1}", True, (255, 255, 255))
        pygame.draw.circle(screen, (0, 0, 255), coordenada, 10)
        screen.blit(indice_vertice, (coordenada[0] + 10, coordenada[1] - 5))
    
    '''tamanho_caminho = len(caminho_gerado)
    for index in range(tamanho_caminho - 1):
        x = caminho_gerado[index]
        y = caminho_gerado[index + 1]
        pygame.draw.line(screen, (0, 255, 0), vertices_pos[x - 1], vertices_pos[y - 1], 2)
        pygame.draw.circle(screen, (0, 255, 0), vertices_pos[x - 1], 10)
        pygame.draw.circle(screen, (0, 255, 0), vertices_pos[y - 1], 10)'''
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