import random
from collections import deque

class Map:
    def __init__(self, type, graph, treasurepoint):
        self.type = type
        self.treasurepoint = treasurepoint
        self.graph = graph

    def generate_path(self, vertice_inicial):
        grafo = self.graph
        vertice_destino = self.treasurepoint
        
        queue = deque([(vertice_inicial, [vertice_inicial])])
        
        while queue:
            atual, caminho = queue.popleft()
            
            for adjacente in grafo[atual][2]:
                if atual == vertice_destino:
                    return caminho
                
                if adjacente not in caminho:
                    queue.append((adjacente, caminho + [adjacente]))
    
        return None  # Se nenhum caminho for encontrado
