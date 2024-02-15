# Vetor de inteiros
grid_pos = []
for i in range(80, 801, 40):
    for j in range(60, 541, 40):
        index_vertice = len(grid_pos)
        grid_pos.append((index_vertice, i, j))

# Nome do arquivo de texto
nome_arquivo = "coordenadas_vertices_mapa_sketchy.txt"

# Abrir o arquivo em modo de escrita
with open(nome_arquivo, "w") as arquivo:
    # Escrever os números no arquivo
    for tripla in grid_pos:
        arquivo.write(str(tripla[0]) + " " + str(tripla[1]) + " " + str(tripla[2]) + "\n")

print(f"vertices do grid '{nome_arquivo}'.")