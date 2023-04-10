import numpy as np
import os
from utils import calcular_matriz_distancias_bloques
from sklearn.cluster import DBSCAN
from local_search import localsearch_Ntimes_save


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

    # resolver el problema TSP para los 2 subconjuntos mas pequeños, y guardar la solución en un archivo
    soluciones = []
    distances = []
    for i, cluster in enumerate(clusters):
        distance_matrix = calcular_matriz_distancias_bloques(cluster)
        if len(cluster) < 30000:
            localsearch_Ntimes_save(distance_matrix, f'cluster_{i}_solution', 15)