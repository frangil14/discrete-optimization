
import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.cluster import DBSCAN
from utils import _distance_calculator, plot_solution
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

# Creamos una figura vacía
fig, ax = plt.subplots()


max_x = df['x_coor'].max()
min_x = df['x_coor'].min()
max_y = df['y_coor'].max()
min_y = df['y_coor'].min()

grid_size_x = (max_x - min_x)/5 
grid_size_y = (max_y - min_y)/5 

print(grid_size_x)
print(grid_size_y)

# Dividimos el plano en grillas
df['col'] = np.floor(df['x_coor'] / grid_size_x).astype(int)
df['row'] = np.floor(df['y_coor'] / grid_size_y).astype(int)

max_number_columns = df['col'].max()
max_number_rows = df['row'].max()



statuses = []
facility_customers = []
facility_customers_original_index = []
costs = []
# Iterar sobre las regiones
for columna in range(max_number_columns):
    for fila in range(max_number_rows):
    # Seleccionar clientes y facilidades de la celda i, j
        df_temp = df[
            (df["row"] == fila) &
            (df['col'] == columna) ]

        print(df_temp)
        demand = df_temp['demand'].sum()
        print(demand, vehicle_capacity)
        if (demand>vehicle_capacity):
            print("AL HORNO")
        if (demand < vehicle_capacity/2):
            print("ACA PUEDO USAR 1 SOLO AUTO")

# Plotear grilla
for i in range(max_number_columns):
    ax.axvline(x=i*grid_size_x, color='gray', alpha=0.5)
for i in range(max_number_rows):
    ax.axhline(y=i*grid_size_y, color='gray', alpha=0.5)


ax.scatter(x = df['x_coor'], y = df['y_coor'],
        marker='X', color='red',  alpha=0.5, label='Customer')

# Add legend
# ax.legend(facecolor='white', title='Location')

# Add title
plt.title('Customers to supply')

plt.xticks([])
plt.yticks([])

# Mostramos la figura
plt.show()