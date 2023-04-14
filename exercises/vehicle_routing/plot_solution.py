import matplotlib.pyplot as plt
import networkx as nx
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


depot = 0                       
dem_points = list(range(1,customer_count)) # nodes 1, 2, ..., 20

G = nx.complete_graph(customer_count)  

# pick the city (x,y)-coordinates
my_pos = { customer[0] : ( customer[2], customer[3] ) for customer in customers } # pos[i] = (x_i, y_i)


# nx.draw(G, pos=my_pos)
# plt.show()

with open(f'{file}_result.txt', 'r') as file:
    output_data = file.read().rstrip()

lines = output_data.split('\n')
solutions = []

for i in range(1,vehicle_count):
    for j in range(len(lines[i].split())-1):

        solutions.append((int(lines[i].split()[j]),int(lines[i].split()[j+1])))


A = nx.Graph()
A.add_edges_from(solutions)

nx.draw(G.edge_subgraph(solutions), pos=my_pos, with_labels=True)
plt.show()