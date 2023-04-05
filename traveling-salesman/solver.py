#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import os
import sys
import six
sys.modules['sklearn.externals.six'] = six
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances


import mlrose

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    # print(point1)
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Función que calcula la longitud de una ruta
def calcular_longitud_ruta(ciudades, ruta):
    longitud = 0
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % len(ruta)]
        longitud += length(ciudades[ciudad_actual] , ciudades[ciudad_siguiente])  
    return longitud

# Función que genera una solución inicial aleatoria
def generar_solucion_inicial(num_ciudades):
    ruta = np.arange(num_ciudades)
    np.random.shuffle(ruta)
    return ruta

# Función que implementa la técnica de dos-opt
def dos_opt(ciudades, ruta):
    mejor_ruta = ruta.copy()
    mejor_longitud = calcular_longitud_ruta(ciudades, ruta)
    for i in range(1, len(ruta)-2):
        for j in range(i+1, len(ruta)):
            if j-i == 1: continue
            nueva_ruta = ruta.copy()
            nueva_ruta[i:j] = ruta[j-1:i-1:-1]
            nueva_longitud = calcular_longitud_ruta(ciudades, nueva_ruta)
            if nueva_longitud < mejor_longitud:
                mejor_ruta = nueva_ruta
                mejor_longitud = nueva_longitud
    return mejor_ruta, mejor_longitud

# Función que implementa la búsqueda local
def busqueda_local(ciudades, num_iteraciones):
    mejor_ruta = generar_solucion_inicial(len(ciudades))
    mejor_longitud = calcular_longitud_ruta(ciudades, mejor_ruta)
    
    for i in range(num_iteraciones):
        print(i)
        nueva_ruta = generar_solucion_inicial(len(ciudades))
        nueva_ruta, _ = dos_opt(ciudades, nueva_ruta)
        nueva_longitud = calcular_longitud_ruta(ciudades, nueva_ruta)
        if nueva_longitud < mejor_longitud:
            mejor_ruta = nueva_ruta
            mejor_longitud = nueva_longitud
    
    return mejor_ruta, mejor_longitud



def get_distance_matrix(city_coordinates):


    distances_upper = euclidean_distances(city_coordinates)
    distances_upper[np.triu_indices(len(city_coordinates))] = np.inf

    # Copia los valores reflejados en la mitad inferior de la matriz
    distances_lower = distances_upper.T.copy()

    # Combina las dos mitades en una sola matriz de distancias
    distances = np.minimum(distances_upper, distances_lower)

    return distances

    n = len(city_coordinates)
    distance_matrix = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i, n):
            # Calcula la distancia euclidiana entre la ciudad i y la ciudad j
            distance = math.sqrt((city_coordinates[i][0] - city_coordinates[j][0]) ** 2 +
                                 (city_coordinates[i][1] - city_coordinates[j][1]) ** 2)
            # Asigna la distancia a la matriz de distancias en ambas direcciones
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    return distance_matrix

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    coords_list = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        coords_list.append((float(parts[0]), float(parts[1])))

    fitness_coords = mlrose.TravellingSales(coords = coords_list)

    # Generar ciudades aleatorias

    # Ejecutar la búsqueda local
    # ruta_optima, longitud_optima = busqueda_local(coords_list, num_iteraciones=1000)

    # print(ruta_optima,longitud_optima)

    distance_matrix = get_distance_matrix(coords_list)

    print(distance_matrix)

    # print(coords_list)

    # No podemos calcular las distancias para todos los puntos cuando tenemos muchas ciudades
    # dist_list = []

    # for i in range(len(coords_list)):
    #     for j in range(len(coords_list)):
    #         if i != j:
    #             # print(coords_list[i], coords_list[j])
    #             dist_list.append((i,j, length(coords_list[i],coords_list[j])))

    # print(dist_list)
    # fitness_dists = mlrose.TravellingSales(distances = dist_list)

    # problem_fit = mlrose.TSPOpt(length = nodeCount, fitness_fn = fitness_coords,
    #                         maximize=False)
    
    problem_no_fit = mlrose.TSPOpt(length = nodeCount, fitness_fn = fitness_coords,
                               maximize=False)
    # build a trivial solution
    # visit the nodes in the order they appear in the file

    # Solve problem using the genetic algorithm
    best_state, best_fitness = mlrose.genetic_alg(problem_no_fit, random_state = 2)


    # best_state, best_fitness = mlrose.genetic_alg(problem_no_fit, mutation_prob = 0.2, 
	# 				      max_attempts = 100, random_state = 2)

    print('The best state found is: ', best_state)

    print('The fitness at the best state is: ', best_fitness)
    solution = range(0, nodeCount)

    # calculate the length of the tour
    # obj = length(points[solution[-1]], points[solution[0]])
    # for index in range(0, nodeCount-1):
    #     obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    # output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


# Para probar localmente

full_path = os.path.realpath(__file__)
filename = os.path.join('data','tsp_33810_1')
path = os.path.join(os.path.dirname(full_path), filename)

with open(path, 'r') as input_data_file:
    input_data = input_data_file.read()
print(solve_it(input_data))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

