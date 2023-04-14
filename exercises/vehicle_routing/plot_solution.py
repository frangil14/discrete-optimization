import networkx as nx
import os
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB


file = 'vrp_200_16_1'

# create a function to separate the rounded capacity inequalities (or subtour elimination)
def rounded_capacity_ineq(m, where):
    
    # check if LP relaxation at this branch-and-bound node has an integer solution
    if where == GRB.Callback.MIPSOL: 
        
        # retrieve the LP solution
        xval = m.cbGetSolution(m._x)
        
        # which edges are selected?
        tour_edges = [ e for e in m._G.edges if xval[e] > 0.5 ]
        
        # if connected, add rounded capacity inequalities (if any are violated)
        if nx.is_connected( m._G.edge_subgraph( tour_edges ) ):
            
            nondepot_edges = [ (i,j) for (i,j) in tour_edges if m._depot not in {i,j} ]
            
            for component in nx.connected_components( m._G.edge_subgraph( nondepot_edges ) ):
                
                component_demand = sum( m._q[i] for i in component )
                
                if component_demand > vehicle_capacity:
                    
                    cut_edges = [ (i,j) for (i,j) in m._G.edges if ( i in component) ^ ( j in component ) ]
                    m.cbLazy( gp.quicksum( m._x[e] for e in cut_edges ) >= 2 * math.ceil( component_demand / m._Q ) )
        
        # else, add subtour elimination constraints for non-depot components
        else: 
            
            for component in nx.connected_components( m._G.edge_subgraph( tour_edges ) ):
                
                if m._depot not in component:
                    
                    inner_edges = [ (i,j) for (i,j) in m._G.edges if i in component and j in component ]
                    m.cbLazy( gp.quicksum( m._x[e] for e in inner_edges ) <= len(component) - 1 )


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

with open('vrp_101_10_1_result.txt', 'r') as file:
    output_data = file.read().rstrip()

lines = output_data.split('\n')
solutions = []

for i in range(1,10):
    for j in range(len(lines[i].split())-1):

        solutions.append((int(lines[i].split()[j]),int(lines[i].split()[j+1])))

# solutions = [ i for i in lines[i].split() ]

# solutions = lines[1].split()

print(solutions)

# G.add_edges_from([(1, 2), (2, 3)], weight=3)


# tour_edges = [ e for e in G.edges if x[e].x > 0.5 ]
A = nx.Graph()
A.add_edges_from(solutions)

# A[0] = (0,0)


# print(A)
# print(G)

# nx.draw(A, pos=my_pos)


nx.draw(G.edge_subgraph(solutions), pos=my_pos, with_labels=True)
plt.show()