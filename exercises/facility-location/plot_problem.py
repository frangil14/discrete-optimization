import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
plt.style.use('ggplot')

# Si dividimos el problema, definimos las dimensiones de la grilla
divide_problem = True
grid_size = 80000

full_path = os.path.realpath(__file__)
filename = os.path.join('data','fl_100_1')
path = os.path.join(os.path.dirname(full_path), filename)

with open(path, 'r') as input_data_file:
    input_data = input_data_file.read()

# parse the input
lines = input_data.split('\n')

parts = lines[0].split()
facility_count = int(parts[0])
customer_count = int(parts[1])

facilities = []
for i in range(1, facility_count+1):
    parts = lines[i].split()
    facilities.append((i-1, float(parts[0]), int(parts[1]), float(parts[2]), float(parts[3])))

customers = []
for i in range(facility_count+1, facility_count+1+customer_count):
    parts = lines[i].split()
    customers.append((i-1-facility_count, int(parts[0]), float(parts[1]), float(parts[2])))


customer_df = pd.DataFrame (customers, columns = ['index', 'demand', 'x_coor', 'y_coor'])
facility_df = pd.DataFrame (facilities, columns = ['index', 'setup_cost', 'capacity', 'x_coor', 'y_coor'])

# Creamos una figura vacía
fig, ax = plt.subplots()

if divide_problem:

    # Dividimos el plano en grillas
    facility_df['col'] = np.floor(facility_df['x_coor'] / grid_size).astype(int)
    facility_df['row'] = np.floor(facility_df['y_coor'] / grid_size).astype(int)

    customer_df['col'] = np.floor(customer_df['x_coor'] / grid_size).astype(int)
    customer_df['row'] = np.floor(customer_df['y_coor'] / grid_size).astype(int)

    max_number_columns = max(facility_df['col'].max()+1,customer_df['col'].max()+1)
    max_number_rows = max(facility_df['row'].max()+1,customer_df['row'].max()+1)

    # Plotear grilla
    for i in range(max_number_columns+1):
        ax.axvline(x=i*grid_size, color='gray', alpha=0.5)
    for i in range(max_number_rows+1):
        ax.axhline(y=i*grid_size, color='gray', alpha=0.5)


ax.scatter(x = customer_df['x_coor'], y = customer_df['y_coor'],
            marker='X', color='red',  alpha=0.5, label='Customer')
ax.scatter(x = facility_df['x_coor'], y = facility_df['y_coor'],
            marker='D', color='blue',  alpha=0.5, label='Potential warehouse')
# Add legend
# ax.legend(facecolor='white', title='Location')

# Add title
plt.title('Customer and potential warehouses')

plt.xticks([])
plt.yticks([])

# Mostramos la figura
plt.show()