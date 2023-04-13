import os
import numpy as np
import pandas as pd
import pulp
import itertools
import matplotlib.pyplot as plt

import math

def length(point1_xcoor, point1_ycoor, point2_xcoor, point2_ycoor):
    return math.sqrt((point1_xcoor - point2_xcoor)**2 + (point1_ycoor - point2_ycoor)**2)

# function for calculating distance between two pins
def _distance_calculator(_df):
    
    _distance_result = np.zeros((len(_df),len(_df)))
    
    for i in range(len(_df)):
        for j in range(len(_df)):
            
            # calculate distance of all pairs
            _distance = length(_df['x_coor'].iloc[i],_df['y_coor'].iloc[i],
                            _df['x_coor'].iloc[j],_df['y_coor'].iloc[j])
            # append distance to result list
            _distance_result[i][j] = _distance
    
    return _distance_result

full_path = os.path.realpath(__file__)
filename = os.path.join('data','vrp_5_4_1')
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



distance = _distance_calculator(df)

# plot_result = _plot_on_gmaps(df)
# plot_result


# solve with pulp
for vehicle_count in range(1,vehicle_count+1):
    
    # definition of LpProblem instance
    problem = pulp.LpProblem("CVRP", pulp.LpMinimize)

    # definition of variables which are 0/1
    x = [[[pulp.LpVariable("x%s_%s,%s"%(i,j,k), cat="Binary") if i != j else None for k in range(vehicle_count)]for j in range(customer_count)] for i in range(customer_count)]

    # add objective function
    problem += pulp.lpSum(distance[i][j] * x[i][j][k] if i != j else 0
                          for k in range(vehicle_count) 
                          for j in range(customer_count) 
                          for i in range (customer_count))

    # constraints
    # foluma (2)
    for j in range(1, customer_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0 
                              for i in range(customer_count) 
                              for k in range(vehicle_count)) == 1 

    # foluma (3)
    for k in range(vehicle_count):
        problem += pulp.lpSum(x[0][j][k] for j in range(1,customer_count)) == 1
        problem += pulp.lpSum(x[i][0][k] for i in range(1,customer_count)) == 1

    # foluma (4)
    for k in range(vehicle_count):
        for j in range(customer_count):
            problem += pulp.lpSum(x[i][j][k] if i != j else 0 
                                  for i in range(customer_count)) -  pulp.lpSum(x[j][i][k] for i in range(customer_count)) == 0

    #foluma (5)
    for k in range(vehicle_count):
        problem += pulp.lpSum(df.demand[j] * x[i][j][k] if i != j else 0 for i in range(customer_count) for j in range (1,customer_count)) <= vehicle_capacity 


    # fomula (6)
    subtours = []
    for i in range(2,customer_count):
         subtours += itertools.combinations(range(1,customer_count), i)

    for s in subtours:
        problem += pulp.lpSum(x[i][j][k] if i !=j else 0 for i, j in itertools.permutations(s,2) for k in range(vehicle_count)) <= len(s) - 1

    
    # print vehicle_count which needed for solving problem
    # print calculated minimum distance value
    if problem.solve() == 1:
        print('Vehicle Requirements:', vehicle_count)
        print('Moving Distance:', pulp.value(problem.objective))
        break
        

# visualization : plotting with matplolib
plt.figure(figsize=(8,8))
for i in range(customer_count):    
    if i == 0:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='green', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], "depot", fontsize=12)
    else:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='orange', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], str(df.demand[i]), fontsize=12)

for k in range(vehicle_count):
    for i in range(customer_count):
        for j in range(customer_count):
            if i != j and pulp.value(x[i][j][k]) == 1:
                plt.plot([df.x_coor[i], df.x_coor[j]], [df.y_coor[i], df.y_coor[j]], c="black")

plt.show()