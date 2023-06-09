import gurobipy as gp
import matplotlib.pyplot as plt
import math
import networkx as nx
import os
from gurobipy import GRB
from utils import rounded_capacity_ineq

def eucl_dist(x1,y1,x2,y2):
    return math.sqrt( (x1-x2)**2 + (y1-y2)**2 )



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

    
customers = []
for i in range(1, customer_count+1):
    line = lines[i]
    parts = line.split()
    customers.append((i-1, int(parts[0]), float(parts[1]), float(parts[2])))


depot = 0                       
dem_points = list(range(1,customer_count)) # nodes 1, 2, ..., 20

G = nx.complete_graph(customer_count)  

# pick the city (x,y)-coordinates
my_pos = { customer[0] : ( customer[2], customer[3] ) for customer in customers } # pos[i] = (x_i, y_i)


# nx.draw(G, pos=my_pos)
# plt.show()


for i,j in G.edges:
    (x1,y1) = my_pos[i]
    (x2,y2) = my_pos[j]
    G.edges[i,j]['length'] = eucl_dist(x1,y1,x2,y2)


q = { customer[0] : customer[1] for customer in customers } # pos[i] = (x_i, y_i)

# First, solve a relaxation

m = gp.Model()
x = m.addVars(G.edges,vtype=GRB.BINARY)

m.setObjective( gp.quicksum( G.edges[e]['length'] * x[e] for e in G.edges ), GRB.MINIMIZE )

# Degree-2 constraints
m.addConstrs( gp.quicksum( x[e] for e in G.edges if e in G.edges(i) ) == 2 for i in dem_points )

# Degree-(2*k) constraints at depot
m.addConstr( gp.quicksum( x[e] for e in G.edges if e in G.edges(0) ) == 2*vehicle_count )

m.update()

# tell Gurobi that we will be adding (lazy) constraints
m.Params.lazyConstraints = 1

# For big problems
m.Params.MIPGap = 0.02

# designate the callback routine 
m._callback = rounded_capacity_ineq

# add the variables and graph to our model object, for use in the callback
m._x = x
m._G = G
m._q = q
m._Q = vehicle_capacity
m._depot = 0

# solve the MIP with our callback
m.optimize(m._callback)

# get the solution and draw it

tour_edges = [ e for e in G.edges if x[e].x > 0.5 ]
cost = m.getObjective().getValue()

result = G.edge_subgraph(tour_edges)

cycles = nx.cycles.cycle_basis(result)



# prepare the solution in the specified output format
outputData = '%.2f' % cost + ' ' + str(0) + '\n'

for cycle in cycles:
    outputData += str(0) + ' ' + ' '.join(map(str, cycle)) + ' ' + '\n'


file = open(f"{file}_result.txt", "a")
a = file.write(outputData)
file.close()


nx.draw(G.edge_subgraph(tour_edges), pos=my_pos, with_labels=True)
plt.show()