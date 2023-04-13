import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass
import os
import numpy as np
import pandas as pd
from pulp import *
import itertools
import matplotlib.pyplot as plt
from facility_location.utils import length

file = 'vrp_26_8_1'


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


distance = _distance_calculator(df)

print(df)


# plot_result = _plot_on_gmaps(df)
# plot_result

final_solution = []
# solve with pulp
for vehicle_count in range(1,vehicle_count+1):
    
    # definition of LpProblem instance
    problem = LpProblem("CVRP", LpMinimize)

    # definition of variables which are 0/1
    x = [[[LpVariable("x%s_%s,%s"%(i,j,k), cat="Binary") if i != j else None for k in range(vehicle_count)]for j in range(customer_count)] for i in range(customer_count)]

    # add objective function
    problem += lpSum(distance[i][j] * x[i][j][k] if i != j else 0
                          for k in range(vehicle_count) 
                          for j in range(customer_count) 
                          for i in range (customer_count))

    # constraints
    # foluma (2)
    for j in range(1, customer_count):
        problem += lpSum(x[i][j][k] if i != j else 0 
                              for i in range(customer_count) 
                              for k in range(vehicle_count)) == 1 

    # foluma (3)
    for k in range(vehicle_count):
        problem += lpSum(x[0][j][k] for j in range(1,customer_count)) == 1
        problem += lpSum(x[i][0][k] for i in range(1,customer_count)) == 1

    # foluma (4)
    for k in range(vehicle_count):
        for j in range(customer_count):
            problem += lpSum(x[i][j][k] if i != j else 0 
                                  for i in range(customer_count)) -  lpSum(x[j][i][k] for i in range(customer_count)) == 0

    #foluma (5)
    for k in range(vehicle_count):
        problem += lpSum(df.demand[j] * x[i][j][k] if i != j else 0 for i in range(customer_count) for j in range (1,customer_count)) <= vehicle_capacity 


    # fomula (6)
    subtours = []
    for i in range(2,customer_count):
         subtours += itertools.combinations(range(1,customer_count), i)

    for s in subtours:
        problem += lpSum(x[i][j][k] if i !=j else 0 for i, j in itertools.permutations(s,2) for k in range(vehicle_count)) <= len(s) - 1

    
    # print vehicle_count which needed for solving problem
    # print calculated minimum distance value

    test = problem.solve(GUROBI(timeLimit=1000))
    print(test)

    # test = problem.solve()
    print(LpStatus[problem.status])

    if test == 1:
        print('Vehicle Requirements:', vehicle_count)
        print('Moving Distance:', value(problem.objective))
        final_solution.append((vehicle_count, problem.objective.value()))
        break
        


print(final_solution)
output = {}

# visualization : plotting with matplolib
plt.figure(figsize=(8,8))
for i in range(customer_count):    
    if i == 0:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='green', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], "depot", fontsize=12)
    else:
        plt.scatter(df.x_coor[i], df.y_coor[i], c='orange', s=200)
        plt.text(df.x_coor[i], df.y_coor[i], str(df.index[i]), fontsize=12)

customers = [int(row['index']) for index, row in df.iterrows()]

for k in range(vehicle_count):
    served_customers = []
    for i in range(customer_count):
        for j in range(customer_count):
            if i != j and value(x[i][j][k]) == 1:
                served_customers.append(customers[i])
                plt.plot([df.x_coor[i], df.x_coor[j]], [df.y_coor[i], df.y_coor[j]], c="black")
    output[k] = served_customers

print(output)
print(total_vehicle_count, vehicle_count )


# prepare the solution in the specified output format
outputData = '%.2f' % final_solution[0][1] + ' ' + str(0) + '\n'
for v in range(0, total_vehicle_count):
    try:
        outputData += ' '.join([str(customer) for customer in output[v]]) + ' ' + str(0) + '\n'
    except:
        outputData += str(0) + ' ' + str(0) + '\n'
print(outputData)


file = open(f"{file}_result.txt", "a")
a = file.write(outputData)
file.close()

plt.show()