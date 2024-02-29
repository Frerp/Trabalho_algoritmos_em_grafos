import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ilha dos Perigos")

clock = pygame.time.Clock()

background_image = pygame.image.load('mapa_ilha10.jpeg')
background_image = pygame.transform.scale(background_image, (800, HEIGHT))

# Coordenadas dos vértices
vertices_pos = []
vertices_grid = "coordenadas_vertices.txt"

with open(vertices_grid, "r") as arquivo:
    for linha in arquivo:
        tripla = linha.split()
        coord_x = int(tripla[1])
        coord_y = int(tripla[2])
        vertices_pos.append((coord_x, coord_y))

# Lista de adjacências
lista_adjacencias = {
    1: [3, 4],
    2: [9, 3],
    3: [6, 1],
    4: [6, 11],
    5: [8, 14],
    6: [3, 10],
    7: [11, 12],
    8: [9, 5],
    9: [8, 2],
    10: [15, 6],
    11: [16, 7],
    12: [22, 17],
    13: [17, 12],
    14: [8, 18],
    15: [10, 26],
    16: [11, 27],
    17: [13, 22],
    18: [23, 14],
    19: [25, 24],
    20: [15, 10],
    21: [26, 27],
    22: [28, 12],
    23: [18, 24],
    24: [23, 29],
    25: [35, 19],
    26: [21, 15],
    27: [31, 21],
    28: [22, 32],
    29: [23, 24],
    30: [35, 40],
    31: [27, 32],
    32: [28, 37],
    33: [34, 32],
    34: [33, 28],
    35: [30, 25],
    36: [41, 26],
    37: [46, 32],
    38: [29, 35],
    39: [40, 35],
    40: [39, 42],
    41: [42, 36],
    42: [41, 40],
    43: [44, 45],
    44: [43, 45],
    45: [43, 44],
    46: [37, 45],
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    # Desenha as linhas entre os vértices adjacentes
    for vertice, adjacentes in lista_adjacencias.items():
        for adjacente in adjacentes:
            pygame.draw.line(screen, (255, 0, 0), vertices_pos[vertice - 1], vertices_pos[adjacente - 1], 2)

    # Desenha os vértices
    for pos in vertices_pos:
        pygame.draw.circle(screen, (0, 255, 0), pos, 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
