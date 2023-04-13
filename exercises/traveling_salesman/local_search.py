import numpy as np
from python_tsp.heuristics import *
from python_tsp.exact import *

def localsearch_Ntimes_save(distance_matrix, fileName, n=10):

    initial_cost = np.inf

    for j in range(n):

        print(f'Iteration number {j}')
        permutation, distance = solve_tsp_local_search(distance_matrix)

        if distance < initial_cost:
            initial_cost = distance
            print(initial_cost)
            final_solution = permutation

    last_point = final_solution[-1]
    output_data = '%.2f' % initial_cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, final_solution)) + '\n'
    file = open(f"{fileName}.txt", "a")
    a = file.write(output_data)
    file.close()

    return last_point