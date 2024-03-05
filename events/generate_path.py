import random
from collections import deque

def generate_path(grafo):
    vertices_inicio = [1, 2, 7]
    vertices_tesouro = [13, 17, 20, 33, 34, 40, 42, 43, 44, 45, 46, 47, 48]

    vertice_inicial = random.choice(vertices_inicio)
    vertice_destino = random.choice(vertices_tesouro)

    queue = deque([(vertice_inicial, [vertice_inicial])])
    
    while queue:
        atual, caminho = queue.popleft()
        
        for adjacente in grafo[atual]:
            if atual == vertice_destino:
                caminho_retornado = []
                tamanho_caminho = len(caminho)

                for index in range(tamanho_caminho - 1):
                    caminho_retornado.append((caminho[index], caminho[index + 1]))

                return vertice_inicial, caminho_retornado
            
            if adjacente not in caminho:
                queue.append((adjacente, caminho + [adjacente]))
   
    return None  # Se nenhum caminho for encontrado
