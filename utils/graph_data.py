def load_graph_data(file_path):
    with open(file_path, "r") as arquivo:
        lista_adjacencias = {}
        for linha in arquivo:
            vertice_id, adjacentes_str = linha.split(":")
            vertice_id = int(vertice_id.strip())
            adjacentes = [int(i.strip()) for i in adjacentes_str.strip()[1:-1].split(',')]
            lista_adjacencias[vertice_id] = adjacentes
    return lista_adjacencias
def load_coordinates_data(file_path):
    with open(file_path, "r") as arquivo:
        vertices_pos = []
        for linha in arquivo:
            tripla = linha.split()
            coord_x = int(tripla[1])
            coord_y = int(tripla[2])
            vertices_pos.append((coord_x, coord_y))
    return vertices_pos
