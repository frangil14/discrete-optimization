import os
from utils import calcular_matriz_distancias_bloques, plot_solution


file = 'tsp_33810_1'

full_path = os.path.realpath(__file__)
filename = os.path.join('solutions',f'{file}_result.txt')
path = os.path.join(os.path.dirname(full_path), filename)

with open(path, 'r') as input_data_file:
    input_data = input_data_file.read()

# parse the input
lines = input_data.split('\n')
list_of_strings = lines[1].split(' ')
list_of_integers = [int(x) for x in list_of_strings]
distance = lines[0].split(' ')[0]


full_path = os.path.realpath(__file__)
filename = os.path.join('data',file)
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

print("Final distance", distance)

plot_solution(coords_list, solution=list_of_integers)