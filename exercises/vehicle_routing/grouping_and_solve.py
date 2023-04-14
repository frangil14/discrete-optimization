import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.cluster import DBSCAN
from utils import _distance_calculator, plot_solution
import numpy as np
from python_tsp.exact import *

file = 'vrp_101_10_1'


full_path = os.path.realpath(__file__)
filename = os.path.join('data',file)
path = os.path.join(os.path.dirname(full_path), filename)

with open(path, 'r') as input_data_file:
    input_data = input_data_file.read()    

lines = input_data.split('\n')

parts = lines[0].split()
customer_count = int(parts[0])
vehicle_count = int(parts[1])
vehicle_capacity = int(parts[2])

total_vehicle_count = vehicle_count
    
customers = []
for i in range(1, customer_count+1):
    line = lines[i]
    parts = line.split()
    customers.append((i-1, int(parts[0]), float(parts[1]), float(parts[2])))



df = pd.DataFrame (customers, columns = ['index', 'demand', 'x_coor', 'y_coor'])
df_copy = df.copy()

df_copy = df_copy.drop(0)


distance = _distance_calculator(df)

max = distance.max()

# para tener 3 clusters, eps = int(max/40)

dbscan = DBSCAN(eps=int(max/10), min_samples=5)

coords_list = [(row['x_coor'], row['y_coor']) for index, row in df_copy.iterrows()]

dbscan.fit(coords_list)

labels = dbscan.labels_
n_clusters = len(np.unique(labels))




df_copy['label'] = 0

for i in range(len(df_copy)):
    df_copy['label'].iloc[i] = labels[i]


solutions = {}
for i in range(n_clusters):

    temp_df = df_copy[
    (df_copy["label"] == i)]

    distance_matrix = _distance_calculator(temp_df)
    temp_df.reset_index(inplace=True)
    print(temp_df)

    print(f'Iteration number {i}')
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    permutation_original_index = []

    for item in permutation:
        temp = temp_df.iloc[item]['level_0']
        permutation_original_index.append(int(temp))

    solutions[i] = ( permutation_original_index, distance)

print(solutions)

cost = 0


for item in list(solutions.values()):
    cost =+ item[1]

# prepare the solution in the specified output format
outputData = '%.2f' % cost + ' ' + str(0) + '\n'

for item in list(solutions.values()):
    outputData += str(0) + ' ' + ' '.join(map(str, item[0])) + ' ' + str(0) + '\n'

# print(list(solutions.values()))



# for key, item in solutions.items():
#     outputData += str(0) + ' ' + ' '.join(map(str, item[0])) + ' ' + '\n'


print(outputData)
file = open(f"{file}_result.txt", "a")
a = file.write(outputData)
file.close()