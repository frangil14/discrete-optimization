import matplotlib.pyplot as plt
import pandas as pd
import os

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
# # set depot x_coor and y_coor
# depot_x_coor = 40.748817
# depot_y_coor = -73.985428

# # make dataframe which contains vending machine location and demand
# df = pd.DataFrame({"x_coor":np.random.normal(depot_x_coor, 0.007, customer_count), 
#                    "y_coor":np.random.normal(depot_y_coor, 0.007, customer_count), 
#                    "demand":np.random.randint(10, 20, customer_count)})

# # set the depot as the center and make demand 0 ('0' = depot)
# df['x_coor'].iloc[0] = depot_x_coor
# df['y_coor'].iloc[0] = depot_y_coor
# df['demand'].iloc[0] = 0
# df.iloc[0,0] = depot_x_coor
# df.iloc[0,0].y_coor = depot_y_coor
# df.iloc[0,0].demand = 0




plt.figure(figsize=(8,8))
for i in range(customer_count):    
    if i == 0:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='green', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], "depot", fontsize=12)
    else:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='orange', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], str(df.index[i]), fontsize=12)

plt.show()