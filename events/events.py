import random
from characters.checkpoint import Checkpoint
from characters.enemy import Enemy
from characters.weapon import Weapon
from characters.terreno import Terreno
from characters.heal import Heal
from characters.map import Map
from characters.treasure import Treasure


def generate_random_event():
    evento = random.choice(['inimigo', 'arma', 'cura', 'terreno'])
    if evento == 'inimigo':
        nomeInimigo = random.choice(['Pantera Mística', 'Leão de Nemeia', 'Formigas Quimera', 'Cobra Gigante'])
        if(nomeInimigo == 'Pantera Mística'):
            image_path = 'Assets/pantera.jpeg'
            attack = 15
            health = 50
        elif (nomeInimigo == 'Leão de Nemeia'):
            image_path = 'Assets/leao.jpeg'
            attack = 12
            health = 60
        elif (nomeInimigo == 'Formigas Quimera'):
            image_path = 'Assets/formiga.jpeg'
            attack = 30
            health = 70
        elif (nomeInimigo == 'Cobra Gigante'):
            image_path = 'Assets/cobra.jpeg'
            attack = 20
            health = 65
        objeto = Enemy('inimigo', nomeInimigo, attack, health, image_path)
    elif evento == 'arma':
        damage = random.randint(10, 30)
        objeto = Weapon('arma', damage, 3)
    elif evento == 'cura':
        healing_points = random.randint(15, 30)
        objeto = Heal('cura', healing_points)
    elif evento == 'terreno':
        name = random.choice(['deslizamento_pedra', 'areia_movedica', 'rio_traicoeiros'])
        damage = random.randint(10, 20)
        objeto = Terreno('terreno', name, damage)
    return objeto



def generate_events(graph, beachpoints, checkpoints, treasurepoints):

    #lista de vertices seguros
    lista_vertices_seguros = []
    for item in checkpoints:
        lista_vertices_seguros.append(item)
    for item in beachpoints:
        lista_vertices_seguros.append(item)

    #inicializando lista de eventos vazia
    dicionario_eventos = {}
    for i in range(1, 51):
        dicionario_eventos[i] = None

    #gerando checkpoints
    for i in checkpoints:
        dicionario_eventos[i] = Checkpoint('checkpoint')

    #gerando inimigos
    for i in range(6):
        while True:
            vertice = random.randint(1, 50)
            if (dicionario_eventos[vertice] == None) and (vertice not in lista_vertices_seguros):
                break

        nomeInimigo = random.choice(['onça', 'Floresta viva', 'Meruem', 'Cobra Gigante','Ze Jacare'])
        if(nomeInimigo == 'onça'):
            image_path = 'Assets/onça.png'
            attack = 15
            health = 50
        elif (nomeInimigo == 'Floresta viva'):
            image_path = 'Assets/florestal.png'
            attack = 12
            health = 60
        elif (nomeInimigo == 'Meruem'):
            image_path = 'Assets/formiga quimera.png'
            attack = 30
            health = 70
        elif (nomeInimigo == 'Cobra Gigante'):
            image_path = 'Assets/cobra.png'
            attack = 20
            health = 65
        elif (nomeInimigo == 'Ze Jacare'):
            image_path = 'Assets/Crocodilo_gigante.png'
            attack = 8
            health = 80
        objeto = Enemy('inimigo', nomeInimigo, attack, health, image_path)

        dicionario_eventos[vertice] = objeto

    #gerando perigos do ambiente
    for i in range(4):
        while True:
            vertice = random.randint(1, 50)
            if (dicionario_eventos[vertice] == None) and (vertice not in lista_vertices_seguros):
                break

        name = random.choice(['deslizamento_pedra', 'areia_movedica', 'rio_traicoeiros'])
        if name == 'deslizamento_pedra':
            damage = random.randint(20, 30)
        elif name == 'rio_traicoeiros':
            damage = random.randint(10, 20)
        elif name == 'areia_movedica':
            damage = random.randint(5, 15)
        objeto = Terreno('terreno', name, damage)

        dicionario_eventos[vertice] = objeto

    #gerando armas
    for i in range(3):
        while True:
            vertice = random.randint(1, 50)
            if (dicionario_eventos[vertice] == None) and (vertice not in lista_vertices_seguros):
                break
        
        damage = random.randint(10, 30)
        numero_balas = 3
        objeto = Weapon('arma', damage, numero_balas)

        dicionario_eventos[vertice] = objeto

    #gerando curas
    for i in range(3):
        while True:
            vertice = random.randint(1, 50)
            if (dicionario_eventos[vertice] == None) and (vertice not in lista_vertices_seguros):
                break
        
        healing_points = random.randint(15, 30)
        objeto = Heal('cura', healing_points)

        dicionario_eventos[vertice] = objeto

    #gerando tesouro
    vertice_tesouro = random.choice(treasurepoints)
    quantidade_tesouro = 100
    objeto = Treasure('tesouro', quantidade_tesouro)

    dicionario_eventos[vertice_tesouro] = objeto

    #gerando mapas
    for i in range(1):
        while True:
            vertice = random.randint(1, 50)
            if (dicionario_eventos[vertice] ==  None) and (vertice not in lista_vertices_seguros):
                break
        
        objeto = Map('mapa', graph, vertice_tesouro)
        dicionario_eventos[vertice] = objeto

    return dicionario_eventos
    


    