import numpy as np
import os
from utils import calcular_matriz_distancias_bloques, plot_solution
from python_tsp.heuristics import *


# Función para encontrar el siguiente nodo más cercano
def encontrar_proximo_nodo(distancias, visitados, actual):
    # Obtener la fila correspondiente a la ciudad actual
    fila = distancias[actual, :]
    # Establecer las distancias a las ciudades ya visitadas en infinito
    fila[visitados] = np.inf
    # Encontrar el índice del siguiente nodo más cercano
    siguiente_nodo = np.argmin(fila)
    # Devolver el índice del siguiente nodo y su distancia
    return siguiente_nodo, fila[siguiente_nodo]

# Función para resolver el problema del vendedor viajante utilizando el algoritmo Greedy
def vendedor_viajante_greedy(distancias, initial_point = None):
    # Obtener el número de ciudades
    n = distancias.shape[0]
    # Seleccionar la ciudad inicial al azar
    if initial_point is None:
        ciudad_actual = np.random.randint(0, n)
    else:
        ciudad_actual = initial_point
    # Inicializar la lista de ciudades visitadas
    visitados = [ciudad_actual]
    # Inicializar la distancia total del recorrido
    distancia_total = 0
    # Recorrer todas las ciudades
    for i in range(n-1):
        # Encontrar el siguiente nodo más cercano
        siguiente_nodo, distancia = encontrar_proximo_nodo(distancias, visitados, ciudad_actual)
        # Agregar el siguiente nodo a la lista de ciudades visitadas
        visitados.append(siguiente_nodo)
        # Actualizar la distancia total del recorrido
        distancia_total += distancia
        # Establecer la ciudad actual en el siguiente nodo
        ciudad_actual = siguiente_nodo
    # Agregar la ciudad inicial al final del recorrido para completar el circuito
    #visitados.append(visitados[0])
    # Calcular la distancia desde la última ciudad visitada a la ciudad inicial
    distancia_total += distancias[visitados[-1], visitados[0]]
    # Devolver la lista de ciudades visitadas y la distancia total del recorrido
    return visitados, distancia_total


if __name__ == '__main__':

    initial_cost = np.inf
    for j in range(10000):
        full_path = os.path.realpath(__file__)
        filename = os.path.join('data','tsp_1889_1')
        path = os.path.join(os.path.dirname(full_path), filename)

        with open(path, 'r') as input_data_file:
            input_data = input_data_file.read()

        # parse the input
        lines = input_data.split('\n')
        nodeCount = int(lines[0])
        coords_list = []
        for i in range(1, nodeCount+1):
            line = lines[i]
            parts = line.split()
            coords_list.append((float(parts[0]), float(parts[1])))

        distance_matrix = calcular_matriz_distancias_bloques(coords_list)
        solution, cost = vendedor_viajante_greedy(distance_matrix)

        if cost < initial_cost:
            initial_cost = cost
            print(initial_cost)
            final_solution = solution

    permutation, distance = solve_tsp_local_search(distance_matrix, x0=final_solution)

    output_data = '%.2f' % distance + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, permutation))
    file = open(f"tsp_1889_1_result.txt", "a")
    a = file.write(output_data)
    file.close()
    plot_solution(coords_list, solution=permutation)