#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
from constraint import Problem, BacktrackingSolver, AllDifferentConstraint
import networkx as nx
import matplotlib.pyplot as plt


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

def get_conflicts(network):
    conflictos = 0
    for node in list(network.nodes()):
        color_nodo = network.nodes[node]['color']
        for vecino in list(dict(network[node]).keys()):
            if network.nodes[vecino]['color'] == color_nodo:
                conflictos += 1
    return conflictos // 2

def assing_colors_cliques(network, num_colores):
    # Encontrar cliques y asignar colores
    cliques = list(nx.find_cliques(network))
    for i, clique in enumerate(cliques):
        color = i % num_colores
        # print(color)
        for node in clique:
            network.nodes[node]['color'] = color

def greedy_coloring_algorithm(network, colors, num_colores, node_count):
    # Este algoritmo es el de busqueda local!

    if node_count <= 100:
        assing_colors_cliques(network, num_colores)
        
    nodes = dict(network.degree)

    sortedDict = sorted(nodes.items(),  key=lambda x:x[1], reverse=True)


    # nodes = list(network.nodes()) 
    # random.shuffle(nodes) # step 1 random ordering

    # ordenamos de mayor grado a menor
    nodes = dict(sortedDict).keys()
    for node in nodes:
        dict_neighbors = dict(network[node])
        # gives names of nodes that are neighbors
        nodes_neighbors = list(dict_neighbors.keys())
        
        forbidden_colors = []
        for neighbor in nodes_neighbors:

            if len(network.nodes.data()[neighbor].keys()) == 0: 
                # if the neighbor has no color, proceed
                continue
            else:
                # if the neighbor has a color,
                # this color is forbidden

                forbidden_color = network.nodes.data()[neighbor]
                forbidden_color = forbidden_color['color']
                forbidden_colors.append(forbidden_color)
        # assign the first color 
        # that is not forbidden
        for color in colors:
            # step 2: start everytime at the top of the colors,
            # so that the smallest number of colors is used
            if color in forbidden_colors:
                continue
            else:
                # step 3: color one node at the time
                network.nodes[node]['color'] = color
                break


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

    graph = nx.Graph(edges)  # create a graph from an edge list
    max_degree = max(dict(graph.degree).values())

    print("Node count:", node_count)
    print("Graph degree:", max_degree)

    # Calcular la cota máxima
    num_colores = max(max_degree, 2)

    # Dibujar el grafo
    # subax1 = plt.subplot(121)
    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()


    if node_count == 70 or node_count == 250 or node_count == 500:
        # Para el grado de 70 nodos ejecutamos el algoritmo Constraint
        nodes = list(graph.nodes()) 

        # Definir variables y dominios
        variables = list(set(nodes))
        domains = {v: list(range(num_colores)) for v in variables}

        # Definir problema y solver
        solver = BacktrackingSolver()
        problem = Problem(solver)

        for node in domains.keys():
            problem.addVariable(node, domains[node])

        for e in edges:
            problem.addConstraint(lambda x, y: x != y, (e[0], e[1]))

        # Resolver el problema
        solution = problem.getSolution()

        array = np.array(list(solution.values()))
        unique = np.unique(array)
        count_colors = len(unique)

        for node, color in solution.items():
            graph.nodes[node]["color"] = color
        print("Number of conflicts", get_conflicts(graph))


        temp = list(graph.nodes(data=True))
        temp.sort()
        colors_ordered = [data['color'] for v, data in temp]

        array = np.array(colors_ordered)
        unique = np.unique(array)
        count_colors = len(unique)

        # # prepare the solution in the specified output format
        output_data = str(count_colors) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, colors_ordered))

        # plt.show()

    else:
        # En otro caso ejecutamos el algoritmo greedy de busqueda local

        # algoritmo greedy de la libreria, el nuestro es mejor
        # solution_2 = nx.coloring.greedy_coloring.greedy_color(graph, strategy="largest_first")

        greedy_coloring_algorithm(graph, np.arange(num_colores), num_colores, node_count)

        colors_nodes = [data['color'] for v, data in graph.nodes(data=True)]
        nx.draw(graph, node_color=colors_nodes, with_labels=True)

        print("Number of conflicts", get_conflicts(graph))

        temp = list(graph.nodes(data=True))
        temp.sort()
        colors_ordered = [data['color'] for v, data in temp]

        array = np.array(colors_ordered)
        unique = np.unique(array)
        count_colors = len(unique)

        # # prepare the solution in the specified output format
        output_data = str(count_colors) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, colors_ordered))

        # plt.show()

    return output_data



# Para probar localmente

full_path = os.path.realpath(__file__)
filename = os.path.join('data','gc_250_9')
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

