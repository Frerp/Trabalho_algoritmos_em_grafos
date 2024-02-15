import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ilha dos Perigos")

clock = pygame.time.Clock()

background_image = pygame.image.load('mapa_ilha10.jpeg')
background_image = pygame.transform.scale(background_image, (800, HEIGHT))

grid_pos = []
vertices_grid = "coordenadas_vertices_mapa_sketchy.txt"
# Abrir o arquivo em modo de leitura
with open(vertices_grid, "r") as arquivo:
    # Puxar coordenadas do arquivo e colocar em duplas no vetor
    for linha in arquivo:
        tripla = linha.split()
        coord_x = int(tripla[1])
        coord_y = int(tripla[2])
        grid_pos.append((coord_x, coord_y))
grid = pygame.Surface((5, 5))
grid.fill((0, 0, 0))

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    for pos in grid_pos:
        screen.blit(grid, pos)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()
