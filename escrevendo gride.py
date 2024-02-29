import math

def calcular_distancia(v1, v2):
    return math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)

def gerar_lista_adjacencia(vertices):
    lista_adjacencia = {}

    for i, v1 in enumerate(vertices):
        lista_adjacencia[i + 1] = []

        # Calcula as distâncias entre o vértice atual e os outros vértices
        distancias = [(j + 1, calcular_distancia(v1, v2)) for j, v2 in enumerate(vertices) if j != i]

        # Ordena as distâncias em ordem crescente
        distancias.sort(key=lambda x: x[1])

        # Adiciona os dois vértices mais próximos à lista de adjacência
        for adjacente, _ in distancias[:2]:
            lista_adjacencia[i + 1].append(adjacente)

    return lista_adjacencia

# Lista de vértices fornecida
lista_de_vertices = [
    (384, 556), (282, 485), (387, 481), (494, 499), (150, 451),
    (437, 429), (589, 447), (190, 404), (251, 403), (357, 401),
    (539, 402), (648, 365), (719, 364), (135, 358), (406, 334),
    (551, 350), (702, 323), (74, 315), (208, 311), (322, 306),
    (485, 293), (640, 303), (79, 257), (142, 272), (212, 237),
    (421, 251), (557, 265), (672, 264), (115, 201), (284, 206),
    (564, 201), (641, 206), (715, 186), (751, 231), (227, 170),
    (446, 164), (616, 142), (156, 137), (275, 120), (334, 149),
    (403, 124), (370, 87), (521, 93), (484, 34), (569, 30),
    (650, 90)
]

# Gera a lista de adjacência
lista_de_adjacencia = gerar_lista_adjacencia(lista_de_vertices)

# Imprime a lista de adjacência
for vertice, adjacentes in lista_de_adjacencia.items():
    print(f"{vertice}: {adjacentes}")
