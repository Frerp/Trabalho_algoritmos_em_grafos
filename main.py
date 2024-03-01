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
1: [2, 3],
2: [1, 9, 10, 3],
3: [1, 4, 6, 2],
4: [3, 6, 7],
5: [8, 14],
6: [3, 10, 4, 15],
7: [4, 11, 12],
8: [9, 5, 14],
9: [8, 2, 10],
10: [2, 9, 15, 6],
11: [16, 7],
12: [13, 22, 16, 17, 7],
13: [17, 12],
14: [8, 18, 5, 19],
15: [6, 10, 21],
16: [21, 11, 12, 22],
17: [13, 22, 12],
18: [23, 14],
19: [25, 14],
20: [30],
21: [15, 16, 27],
22: [28, 12, 16, 17, 27],
23: [18, 24, 29],
24: [23, 25],
25: [30, 24, 19],
26: [30],
27: [21, 22, 28],
28: [22, 27, 32, 34],
29: [23, 38],
30: [20, 25, 26, 35, 40],
31: [32, 36, 37],
32: [28, 37, 33, 31],
33: [37, 34, 32],
34: [33, 28],
35: [30, 38, 39],
36: [31, 40, 41],
37: [46, 43, 33, 32, 31],
38: [29, 35],
39: [40, 35],
40: [36, 39, 41, 30],
41: [42, 43, 40, 36],
42: [41],
43: [37, 41, 44, 45],
44: [43, 45],
45: [43, 44],
46: [37,],
}

font = pygame.font.Font(None, 36)

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

    # Desenha os vértices e seus números
    for vertice, pos in enumerate(vertices_pos, start=1):
        pygame.draw.circle(screen, (0, 255, 0), pos, 10)
        text = font.render(str(vertice), True, (255, 255, 255))
        screen.blit(text, (pos[0] + 12, pos[1]))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
