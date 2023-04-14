
import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.cluster import KMeans
from utils import _distance_calculator, plot_solution, distance_calculator_testing
import numpy as np
from python_tsp.exact import *

file = 'vrp_200_16_1'

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


# distance = _distance_calculator(df)

# max = distance.max()

# para tener 3 clusters, eps = int(max/40)

dbscan = KMeans(n_clusters=16)

coords_list = [(row['x_coor'],row['y_coor']) for index, row in df_copy.iterrows()]

data_to_train = [row['demand'] for index, row in df_copy.iterrows()]
np_array = np.array(data_to_train).reshape(-1, 1)

distance_matrix = distance_calculator_testing(df_copy, vehicle_capacity)


dbscan.fit(distance_matrix)

labels = dbscan.labels_
np.append(labels,0)
n_clusters = len(np.unique(labels))




df_copy['label'] = 0

for i in range(len(df_copy)):
    df_copy['label'].iloc[i] = labels[i]


solutions = {}
for i in range(n_clusters):

    temp_df = df_copy[
    (df_copy["label"] == i)]

    max_demand = temp_df['demand'].sum()
    if (max_demand>vehicle_capacity):
        print('al horno')

plot_solution(coords_list,labels=labels)

