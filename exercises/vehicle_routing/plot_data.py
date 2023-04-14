import matplotlib.pyplot as plt
import pandas as pd
import os

file = 'vrp_421_41_1'


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

    
customers = []
for i in range(1, customer_count+1):
    line = lines[i]
    parts = line.split()
    customers.append((i-1, int(parts[0]), float(parts[1]), float(parts[2])))



df = pd.DataFrame (customers, columns = ['index', 'demand', 'x_coor', 'y_coor'])


plt.figure(figsize=(8,8))
for i in range(customer_count):    
    if i == 0:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='green', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], "depot", fontsize=12)
    else:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='orange', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], str(df.index[i]), fontsize=12)

plt.show()