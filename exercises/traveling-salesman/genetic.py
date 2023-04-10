import mlrose
import os
import sys
import six
sys.modules['sklearn.externals.six'] = six
from utils import calcular_matriz_distancias_bloques, plot_solution

def genetic(distance_matrix, nodeCount):
    # Solve problem using the genetic algorithm

    dist_list = []
    n = len(distance_matrix)
    for i in range(n):
        for j in range(i+1, n):
            dist_list.append((i,j,distance_matrix[i][j]))

    dist_list_full = dist_list + dist_list[::-1]

    fitness_dists = mlrose.TravellingSales(distances = dist_list_full)


    problem_fit = mlrose.TSPOpt(length = nodeCount, fitness_fn = fitness_dists,
                            maximize=False)

    permutation, distance = mlrose.genetic_alg(problem_fit, mutation_prob = 0.2, 
					      max_attempts = 10, random_state = 2)
    
    return permutation, distance


# Para probar localmente
if __name__ == '__main__':

    full_path = os.path.realpath(__file__)
    filename = os.path.join('data','tsp_574_1')
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

    solution, distance = genetic(distance_matrix, nodeCount)

    # prepare the solution in the specified output format
    output_data = '%.2f' % distance + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    plot_solution(coords_list, solution=solution)