import numpy as np
import os
from greedy import vendedor_viajante_greedy
from python_tsp.heuristics import *
from sklearn.cluster import DBSCAN
from utils import plot_solution, calcular_matriz_distancias_bloques, get_score


def grouping_and_greedy(coords_list, total_distance_matrix):

    max = total_distance_matrix.max()

    # para tener 3 clusters, eps = int(max/40)

    dbscan = DBSCAN(eps=int(max/40), min_samples=5)
    dbscan.fit(coords_list)

    labels = dbscan.labels_
    n_clusters = len(np.unique(labels))

    print(f'The {n_clusters} clusters have been created')

    # crear un subconjunto de ciudades para cada cluster
    clusters = []
    for i in range(n_clusters):
        cluster = [coords_list[j] for j in range(len(coords_list)) if labels[j] == i]
        clusters.append(cluster)

    temp = clusters[1]
    clusters[1] = clusters[0]
    clusters[0] = temp

    # resolver el problema TSP para cada subconjunto de ciudades
    soluciones = []
    distances = []
    for i, cluster in enumerate(clusters):
        print(f'Calculating cluster {i}')

        if len(cluster) < 30000:
            distance_matrix = calcular_matriz_distancias_bloques(cluster)
            distance_matrix[:, 0] = 0
            initial_cost = np.inf
            for j in range(10):
                permutation, distance = solve_tsp_local_search(distance_matrix)
                if distance < initial_cost:
                    initial_cost = distance
                    print(initial_cost)
                    final_solution = permutation
                last_point = final_solution[-1]
            print(f'last point {last_point}, coordenates {cluster[last_point]}')
        else:
            distance_matrix = calcular_matriz_distancias_bloques(cluster)
            # distance_matrix[:, 0] = 0
            final_solution, initial_cost = vendedor_viajante_greedy(distance_matrix, last_point)

        distances.append(initial_cost)
        soluciones.append(final_solution)


    # crear un diccionario para mapear cada coordenada a su índice en la lista
    coordenadas_dict = {coordenada: i for i, coordenada in enumerate(coords_list)}

    # combinar las soluciones de los subproblemas
    solucion_completa = []
    for i in range(n_clusters):
        cluster = clusters[i]
        indices = [coordenadas_dict[city] for city in cluster]
        solucion = soluciones[i]
        solucion = [indices[j] for j in solucion]
        solucion_completa.extend(solucion)

    # mostrar la solución completa
    array = np.array(solucion_completa)
    unique = np.unique(array)
    count_cities = len(unique)

    costo = get_score(solucion_completa, total_distance_matrix)

    print("Quantity of cities in the solution", count_cities)
    print("Final distance", costo)

    return solucion_completa, costo


# Para probar localmente

if __name__ == '__main__':

    full_path = os.path.realpath(__file__)
    filename = os.path.join('data','tsp_33810_1')
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


    total_distance_matrix = calcular_matriz_distancias_bloques(coords_list)
    max = total_distance_matrix.max()

    # para tener 3 clusters, eps = int(max/40)

    dbscan = DBSCAN(eps=int(max/40), min_samples=5)
    dbscan.fit(coords_list)

    labels = dbscan.labels_
    n_clusters = len(np.unique(labels))

    print(f'The {n_clusters} clusters have been created')

    # crear un subconjunto de ciudades para cada cluster
    clusters = []
    for i in range(n_clusters):
        cluster = [coords_list[j] for j in range(len(coords_list)) if labels[j] == i]
        clusters.append(cluster)

    temp = clusters[1]
    clusters[1] = clusters[0]
    clusters[0] = temp

    # crear un diccionario para mapear cada coordenada a su índice en la lista
    coordenadas_dict = {coordenada: i for i, coordenada in enumerate(coords_list)}

    initial_cost = np.inf
    for j in range(10):
        print(f'Iteration number {j}')

        # Leo la solución para los 2 subconjuntos mas pequeños, e itero sobre el subconjunto mas grande y complicado
        soluciones = []
        distances = []
        for i, cluster in enumerate(clusters):

            if len(cluster) < 30000:
                fileName = f'cluster_{i}_solution.txt'

                with open(fileName, 'r') as input_data_file:
                    input_data = input_data_file.read()

                # parse the input
                lines = input_data.split('\n')
                list_of_strings = lines[3].split(' ')

                solution = [int(x) for x in list_of_strings]
            else:
                distance_matrix = calcular_matriz_distancias_bloques(cluster)
                # distance_matrix[:, 0] = 0
                solution, costo_greedy = vendedor_viajante_greedy(distance_matrix)#, last_point)

            soluciones.append(solution)

        important_points = []

        # combinar las soluciones de los subproblemas
        solucion_completa = []
        for i in range(n_clusters):
            cluster = clusters[i]
            indices = [coordenadas_dict[city] for city in cluster]
            solucion = soluciones[i]
            solucion = [indices[j] for j in solucion]
            print(solucion[0], solucion[-1])
            important_points.append(coords_list[solucion[0]])
            important_points.append(coords_list[solucion[-1]])
            solucion_completa.extend(solucion)

        # mostrar la solución completa
        array = np.array(solucion_completa)
        unique = np.unique(array)
        count_cities = len(unique)

        costo = get_score(solucion_completa, total_distance_matrix)

        print("Quantity of cities in the solution", count_cities)
        print("Final distance", costo)

        if costo < initial_cost:
            initial_cost = costo
            print(initial_cost)
            final_solution = solucion_completa


    output_data = '%.2f' % initial_cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, final_solution))
    file = open(f"tsp_33810_1_result.txt", "a")
    a = file.write(output_data)
    file.close()

    plot_solution(coords_list,solution=final_solution,different_points=important_points)