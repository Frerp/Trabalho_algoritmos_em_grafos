import random

def determina_proximo_vertice(grafo_global, vertice_atual_global, pilha_global):
    grafo = grafo_global
    pilha = pilha_global
    vertice_atual = vertice_atual_global
    qtd_visitados = grafo[vertice_atual][1]

    grafo[vertice_atual][0] = "cinza"
    if (len(pilha) != 0):
        if (vertice_atual != pilha[-1]):
            pilha.append(vertice_atual)
    else:
        pilha.append(vertice_atual)

    while ( qtd_visitados < len(grafo[vertice_atual][2]) ):
        if ( qtd_visitados < len(grafo[vertice_atual][2]) - 1):
            proximo_vertice = random.choice(grafo[vertice_atual][2][qtd_visitados:])
        else:
            proximo_vertice = grafo[vertice_atual][2][-1]

        if (grafo[proximo_vertice][0] == "branco"):
            index_proximo_vertice = grafo[vertice_atual][2].index(proximo_vertice)
            grafo[vertice_atual][2][index_proximo_vertice] = grafo[vertice_atual][2][qtd_visitados]
            grafo[vertice_atual][2][qtd_visitados] = proximo_vertice
            qtd_visitados += 1
            grafo[vertice_atual][1] = qtd_visitados            
            return grafo, proximo_vertice, pilha
        
        elif (proximo_vertice not in grafo[vertice_atual][2][0:qtd_visitados]):
            index_proximo_vertice = grafo[vertice_atual][2].index(proximo_vertice)
            grafo[vertice_atual][2][index_proximo_vertice] = grafo[vertice_atual][2][qtd_visitados]
            grafo[vertice_atual][2][qtd_visitados] = proximo_vertice
            qtd_visitados += 1
            grafo[vertice_atual][1] = qtd_visitados 
            

    grafo[vertice_atual][0] = "preto"
    pilha.pop()
    if (len(pilha) == 0):
        proximo_vertice = -1
    else:
        proximo_vertice = pilha[-1]
    return grafo, proximo_vertice, pilha
    

