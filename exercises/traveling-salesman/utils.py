import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

def get_score(permutation, distance_matrix):
    temp = 0
    for i in range(len(permutation)-1):
        temp += distance_matrix[permutation[i]][permutation[i+1]]
    temp += distance_matrix[permutation[-1]][permutation[0]]
    return temp

def calcular_matriz_distancias_bloques(coords, bloque_tamano=100):
    num_ciudades = len(coords)
    matriz_distancias = np.zeros((num_ciudades, num_ciudades))
    for i in range(0, num_ciudades, bloque_tamano):
        fin = min(i + bloque_tamano, num_ciudades)
        distancias_bloque = cdist(coords[i:fin], coords)
        matriz_distancias[i:fin, i:num_ciudades] = distancias_bloque[:, i:num_ciudades]
        matriz_distancias[i:num_ciudades, i:fin] = distancias_bloque[:, i:num_ciudades].T
    return matriz_distancias


def plot_solution(coords_list, solution= None, different_points=[],labels=[0]):
    # Define los colores que quieres utilizar para representar cada etiqueta
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k','C0','C1','C2']
    coords_list_np = np.array(coords_list)

    # Crea la figura y grafica las coordenadas
    plt.figure(figsize=(12, 10))
    plt.scatter(coords_list_np[:, 0], coords_list_np[:, 1], c=[colors[label] for label in labels])

    if solution is not None:
        coord_x = [coords_list_np[i][0] for i in solution]
        coord_y = [coords_list_np[i][1] for i in solution]

        plt.plot(coord_x, coord_y)

    if len(different_points)>0:
        different_points_np = np.array(different_points)
        plt.scatter(different_points_np[:, 0], different_points_np[:, 1], c='y')
    # Muestra la figura
    plt.show()