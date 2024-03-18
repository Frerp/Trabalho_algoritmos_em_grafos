import random
from collections import deque

def generate_path(grafo, vertice_inicial, vertice_destino):

    queue = deque([(vertice_inicial, [vertice_inicial])])
    
    while queue:
        atual, caminho = queue.popleft()
        
        for adjacente in grafo[atual][2]:
            if atual == vertice_destino:
                return caminho
            
            if adjacente not in caminho:
                queue.append((adjacente, caminho + [adjacente]))
   
    return None  # Se nenhum caminho for encontrado
