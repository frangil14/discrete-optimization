#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import random
import numpy as np

def matriz_a_lista(matriz):
    lista = {}
    for i in range(len(matriz)):
        adyacentes = []
        for j in range(len(matriz[i])):
            if matriz[i][j] != 0:
                adyacentes.append(j)
        lista[i] = adyacentes
    return lista

def generar_matriz_adyacencia(bordes):
    grafo = {}
    for u, v in bordes:
        if u not in grafo:
            grafo[u] = []
        if v not in grafo:
            grafo[v] = []
        grafo[u].append(v)
        grafo[v].append(u)
    
    vertices = list(grafo.keys())
    n = len(vertices)
    matriz = [[0] * n for _ in range(n)]
    
    for i, u in enumerate(vertices):
        for v in grafo[u]:
            j = vertices.index(v)
            matriz[i][j] = 1

    return matriz



from constraint import Problem, BacktrackingSolver
import networkx as nx
import matplotlib.pyplot as plt


def color_graph(graph, num_colors):
    # Encontrar cliques y asignar colores
    cliques = list(nx.find_cliques(graph))
    colors = {}
    for i, clique in enumerate(cliques):
        color = i % num_colors
        for node in clique:
            colors[node] = color

    # Definir variables y dominios
    variables = list(set(graph.keys()) - set(colors.keys()))
    domains = {v: list(range(num_colors)) for v in variables}

    # Definir restricciones
    constraints = []
    for v, neighbors in graph.items():
        if v in variables:
            for n in neighbors:
                if n in variables:
                    constraints.append((v, n))

    # Definir problema y solver
    problem = Problem(variables, domains, constraints, infer_domains=True)
    solver = BacktrackingSolver()

    # Resolver el problema
    solution = solver.solve(problem, select_min=True)

    # Búsqueda local
    if solution is not None:
        for node, color in solution.items():
            graph.nodes[node]["color"] = color
        solution = nx.coloring.greedy_color(graph, strategy="largest_first")

    # Retornar el resultado
    return solution

# Ejemplo de uso
# num_vertices, edges = read_graph("grafo.txt")
# colors = color_graph(num_vertices, edges)
# if colors is not None:
#     print("El grafo se puede colorear con", len(set(colors)), "colores:")
#     print(colors)
# else:
#     print("El grafo no se puede colorear con un número finito de colores.")

# Example usage
# graph = [[1, 2], [0, 2, 3], [0, 1, 3], [1, 2]]
# colors = ["red", "green", "blue"]
# solve(graph, colors)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    H = nx.Graph(edges)  # create a graph from an edge list

    G = nx.petersen_graph()
    subax1 = plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    subax2 = plt.subplot(122)
    nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')


    # print(edges)
    adj_matrix = generar_matriz_adyacencia(edges)
    print(adj_matrix)

    # Obtener el grado máximo
    grado_maximo = 0
    for i in range(len(adj_matrix)):
        grado = sum(adj_matrix[i])
        if grado > grado_maximo:
            grado_maximo = grado

    print(grado_maximo)
    # Calcular la cota máxima
    num_colores = max(grado_maximo, 2)
    # print(num_colores)

    # build a trivial solution
    # every node has its own color
    my_list = list(matriz_a_lista(adj_matrix).values())
    print(matriz_a_lista(adj_matrix))
    # print(my_list)
    nx.from_numpy
    colors = color_graph(nx.from_numpy_matrix(np.matrix(adj_matrix)), num_colores)
    # solution = solve(my_list, np.arange(num_colores))

    # myKeys = list(solution.keys())
    # myKeys.sort()
    # sorted_dict = {i: solution[i] for i in myKeys}
    
    # print(list(sorted_dict.values()))

    # print("mejor costo", solution[1])

    # solution_2 = range(0, node_count)
    # output_data_2 = ''
    # output_data_2 += ' '.join(map(str, solution_2))
    # print(output_data_2)

    # array = np.array(list(sorted_dict.values()))
    # unique = np.unique(array)
    # count_colors = len(unique)

    # # prepare the solution in the specified output format
    # output_data = str(count_colors) + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, list(sorted_dict.values())))

    return 0



# Para probar localmente

full_path = os.path.realpath(__file__)
filename = os.path.join('data','gc_4_1')
path = os.path.join(os.path.dirname(full_path), filename)

with open(path, 'r') as input_data_file:
    input_data = input_data_file.read()
print(solve_it(input_data))

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

