import pygame
import sys
import random
import copy
from characters.weapon import Weapon
from characters.character import Character
from characters.enemy import Enemy
from characters.checkpoint import Checkpoint
from gui.buttons import Button  # Adicionado import para a classe Button
from utils.graph_data import load_graph_data, load_coordinates_data
from events.events import generate_events
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
caminho_do_mapa = []
#INICIALIZANOD PILHA E CAMINHO GERADO COM BUSCA EM LARGURA


#INICIALIZANDO PROGRESSO DO JOGO
hora = 0
progresso_pilha = []
progresso_lista_adjacencias = {}
progresso_tesouro = 0
ultimo_checkpoint = 0
#INICIALIZANDO PROGRESSO DO JOG


#TESOURO
mochila = {}
qtd_tesouro = 0
#TESOURO


eventos_por_vertice = {}
eventos_por_vertice = generate_events(lista_adjacencias, vertices_inicio, vertices_checkpoints, vertices_tesouro)


vertice_inicial = vertices_pos[index_vertice_inicial  - 1] 
player = Character(vertice_inicial, index_vertice_inicial, health=100, attack=20)


menu_surface = pygame.Surface((MENU_WIDTH, HEIGHT))
menu_surface.fill((50, 50, 50))
running = True

def draw_health_bar(surface, x, y, width, height, health, max_health):
    bar_length = 200
    fill = (health / max_health) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, (255, 0, 0), fill_rect)
    pygame.draw.rect(surface, (0, 0, 0), outline_rect,2)

def draw_treasure_bar(surface, x, y, width, height, treasure_points, max_treasure_points):
    bar_length = 200
    fill = (treasure_points / max_treasure_points) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, (255, 255, 0), fill_rect)
    pygame.draw.rect(surface, (0, 0, 0), outline_rect,2)

calculo_proximo_vertice = 1

while running:
    for event in pygame.event.get():
        
        #DETERMINA ID DO VÉRTICE ATUAL
        vertice_atual = player.current_vertex
        id_vertice_atual = vertices_pos.index(vertice_atual) + 1

        if (id_vertice_atual == index_vertice_inicial) and ('tesouro' in mochila):
            print("VOCÊ GANHOU O JOGO CARAA! QUE LINDO CARAA! QUE LINDOUO!!")
            running = False

        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if player.attack>= 21:  
                event_object_type = Weapon('arma',player.attack-20,player.bullets)
                eventos_por_vertice[id_vertice_atual]= event_object_type
                player.attack = 20
                player.bullets = 0
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            hora += 1
            player.time = hora 
            print("vertice atual: ", id_vertice_atual)

            #LIDANDO COM EVENTO DO VÉRTICE ATUAL
            event_object_type = eventos_por_vertice.get(id_vertice_atual, None)
            if event_object_type:
                event_description = (event_object_type.type)
                print(event_description)

                if 'inimigo' in event_object_type.type:
                    resposta = player.handle_event(event_object_type, screen)
                    if resposta == 'inimigo morreu':
                        eventos_por_vertice[id_vertice_atual] = None
                elif 'cura' in event_object_type.type:
                    resposta =player.handle_event(event_object_type, screen)
                    if resposta == 'cura usada':
                        eventos_por_vertice[id_vertice_atual] = None
                elif'arma' in event_object_type.type: 
                    resposta = player.handle_event(event_object_type, screen)
                    if resposta == 'arma usada':
                        eventos_por_vertice[id_vertice_atual] = None
                elif 'terreno' in event_object_type.type:
                    damage = event_object_type.damage
                    print(f"Você sofreu {damage} de dano devido ao evento.")   
                    player.take_damage(damage)
                    print(f"Sua vida atual: {player.health}")

                elif 'mapa' in event_object_type.type:
                    resposta = player.handle_event(event_object_type, screen)

                    if resposta == 'Peguei o mapa':
                        mochila['mapa'] = event_object_type 
                        if 'tesouro' in mochila:
                            if mochila['tesouro'].treasure_amount > 0:
                                mochila['mapa'].destiny = index_vertice_inicial

                        map = mochila['mapa']
                        caminho_do_mapa = map.generate_path(id_vertice_atual)
                        eventos_por_vertice[id_vertice_atual] = None
                        if len(caminho_do_mapa) > 0:
                            calculo_proximo_vertice = 2
                    elif resposta == 'Deixei o mapa':
                        pass

                elif 'checkpoint' in event_object_type.type:
                    print('Eu entrei no checkpoint')
                    ultimo_checkpoint = id_vertice_atual
                    progresso_pilha = copy.deepcopy(pilha)
                    progresso_lista_adjacencias = copy.deepcopy(lista_adjacencias)
                    eventos_por_vertice[id_vertice_atual] = None
                    player.handle_event(event_object_type, screen)
                    del event_object_type
                    if 'tesouro' in mochila:
                        progresso_tesouro = mochila['tesouro'].treasure_amount

                elif 'tesouro' in event_object_type.type:
                    tesouro = player.handle_event(event_object_type, screen)
                    mochila['tesouro'] = tesouro
                    
                    if 'mapa' in mochila:
                        mochila['mapa'].destiny = index_vertice_inicial
                        caminho_do_mapa = mochila['mapa'].generate_path(id_vertice_atual) 
            #LIDANDO COM EVENTO DO VÉRTICE ATUAL
                    
            if 'tesouro' in mochila:
                qtd_tesouro = mochila['tesouro'].treasure_amount
                if player.health - (player.attack - 20) <= qtd_tesouro: 
                    qtd_tesouro = player.health - (player.attack - 20)

                if qtd_tesouro <= 0:
                    qtd_tesouro = 0
                
                mochila['tesouro'].treasure_amount = qtd_tesouro 

                
                

            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO (USANDO FUNÇÃO DETERMINA_PROXIMO_VERTICE)
            print("\nCABEÇALHO............................................")
            print("vertice atual: ", id_vertice_atual)
            print("cor vertice atual: ", lista_adjacencias[id_vertice_atual][0])
            print("Quantidade tesouro: ", qtd_tesouro)
            print("pilha: ", pilha)
            print("progresso_pilha: ", progresso_pilha)

            if calculo_proximo_vertice == 1:
                lista_adjacencias, proximo_vertice, pilha = determina_proximo_vertice(lista_adjacencias, id_vertice_atual, pilha)
                target_vertex = proximo_vertice
            elif calculo_proximo_vertice == 2:
                posicao_vertice_atual_mapa = caminho_do_mapa.index(id_vertice_atual)
                posicao_target_vertex_caminho_mapa = posicao_vertice_atual_mapa + 1
                if posicao_target_vertex_caminho_mapa < len(caminho_do_mapa):
                    target_vertex = caminho_do_mapa[posicao_target_vertex_caminho_mapa]

            if (target_vertex == -1):
                running = False
            #CÁLCULO DO PRÓXIMO VÉRTICE A SER SEGUIDO NO CAMINHO (USANDO FUNÇÃO DETERMINA_PROXIMO_VERTICE)


            #VERIFICANDO SE PLAYER MORREU E SE TEM CHECKPOINT
            if (player.health <= 0):
                if ultimo_checkpoint > 0:
                    pilha = copy.deepcopy(progresso_pilha)
                    lista_adjacencias = copy.deepcopy(progresso_lista_adjacencias)
                    if 'tesouro' in mochila:
                        mochila['tesouro'].treasure_amount = progresso_tesouro
                    target_vertex = ultimo_checkpoint
                    calculo_proximo_vertice = 1
                    mochila.pop('mapa', "Não há mapa na mochila!")   
                    ultimo_checkpoint = 0
                    player.health = 100
                else:
                    print("Tu morreu mash, tu morreu")
                    pygame.quit()
                    sys.exit()

            player.move_to_vertex(vertices_pos[target_vertex - 1], target_vertex)
            #VERIFICANDO SE PLAYER MORREU E SE TEM CHECKPOINT
            

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))


    #PRINTANDO GRAFO NA TELA PARA AJUDAR VISUALIZAÇÃO
    for vertice, vizinhanca in lista_adjacencias.items():
        for adjacente in vizinhanca[2]:
            pygame.draw.line(screen, (0, 0, 255), vertices_pos[vertice - 1], vertices_pos[adjacente - 1], 2)
    
    fonte = pygame.font.Font(None, 26)
    for coordenada in vertices_pos:
        vertice_index = vertices_pos.index(coordenada) + 1
        indice_vertice = fonte.render(f"{vertices_pos.index(coordenada) + 1}", True, (255, 255, 255))
        if lista_adjacencias[vertice_index][0] == 'branco':
            color = (255, 255, 255)
        elif lista_adjacencias[vertice_index][0] == 'cinza':
            color = (100, 100, 100)
        elif lista_adjacencias[vertice_index][0] == 'preto':
            color = (0, 0, 0)
        pygame.draw.circle(screen, color, coordenada, 10)
        screen.blit(indice_vertice, (coordenada[0] + 10, coordenada[1] - 5))
    
    #GENERATE PATH
    if len(caminho_do_mapa):
        tamanho_caminho = len(caminho_do_mapa)
        for index in range(tamanho_caminho - 1):
            x = caminho_do_mapa[index]
            y = caminho_do_mapa[index + 1]
            pygame.draw.line(screen, (0, 255, 0), vertices_pos[x - 1], vertices_pos[y - 1], 2)
            pygame.draw.circle(screen, (0, 255, 0), vertices_pos[x - 1], 10)
            pygame.draw.circle(screen, (0, 255, 0), vertices_pos[y - 1], 10)
    #GENERATE PATH
    #PRINTANDO GRAFO NA TELA PARA AJUDAR VISUALIZAÇÃO    
            
    player.update_sprite()
    screen.blit(player.image, player.rect.topleft)

    menu_icon = pygame.image.load('Assets/menu_lateral.jpg')
    menu_icon = pygame.transform.scale(menu_icon, (400, 600))
    screen.blit(menu_icon, (800,0))

    if 0 <= hora <= 35:
        pass
        hora_icon = pygame.image.load('Assets/sol icone.png')
    elif 36 <= hora <= 70:
        pass
        hora_icon = pygame.image.load('Assets/meio sol icone.png')
    elif 70 <= hora:
        pass
        hora_icon = pygame.image.load('Assets/lua icone.png')
    hora_icon = pygame.transform.scale(hora_icon, (100, 100))
    screen.blit(hora_icon, (950, 100))

    font = pygame.font.Font(None, 26)
    draw_health_bar(screen, 840, 400, 200, 20, player.health, 100)
    draw_treasure_bar(screen, 840, 370, 200, 20, qtd_tesouro, 100)
    health_text = font.render(f"Vida: {player.health}", True, (0, 0, 0))
    attack_text = font.render(f"Ataque: {player.attack}", True, (0, 0, 0))
    treasure_text = font.render(f"Tesouro: {qtd_tesouro}", True, (0, 0, 0))

    screen.blit(treasure_text, (840, 372))
    screen.blit(health_text, (840, 402))
    screen.blit(attack_text, (840, 342))
    player_icon = pygame.image.load('Assets/Anderson.png')
    player_icon = pygame.transform.scale(player_icon, (150, 150))
    screen.blit(player_icon,(820,420))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()