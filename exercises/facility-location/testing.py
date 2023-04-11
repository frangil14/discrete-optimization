import numpy as np
import os
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from pulp import *

full_path = os.path.realpath(__file__)
filename = os.path.join('data','fl_3_1')
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

customers_coordenates = [(customer[2],customer[3]) for customer in customers]
facilities_coordenates = [(facility[3],facility[4]) for facility in facilities]

facility_costs = [warehouse[1] for warehouse in facilities]
customer_demands = [customer[1] for customer in customers]
facility_capacities = [warehouse[2] for warehouse in facilities]

# coordenadas de los clientes y facilities
clientes = customers_coordenates
facilities = facilities_coordenates

# coordenadas de la grilla
grid_size = 2
min_x = min(min(clientes + facilities, key=lambda x: x[0])[0], 0)
max_x = max(max(clientes + facilities, key=lambda x: x[0])[0], 10)
min_y = min(min(clientes + facilities, key=lambda x: x[1])[1], 0)
max_y = max(max(clientes + facilities, key=lambda x: x[1])[1], 10)
x_grid = np.arange(min_x, max_x + grid_size, grid_size)
y_grid = np.arange(min_y, max_y + grid_size, grid_size)

# asignar cada cliente y facility a su grilla correspondiente
client_assignments = {}
facility_assignments = {}
for i, client in enumerate(clientes):
    x_idx = np.where(x_grid <= client[0])[0][-1]
    y_idx = np.where(y_grid <= client[1])[0][-1]
    client_assignments[i] = (x_idx, y_idx)
    
for i, facility in enumerate(facilities):
    x_idx = np.where(x_grid <= facility[0])[0][-1]
    y_idx = np.where(y_grid <= facility[1])[0][-1]
    facility_assignments[i] = (x_idx, y_idx)

print("Assignments:")
print("Clients: ", client_assignments)
print("Facilities: ", facility_assignments)

# Resolución de subproblemas
# facility_customers = []
# for i in range(len(grid_assignments)):
#     # Seleccionar clientes y facilidades de la celda i
#     cell_customers = np.where(grid_assignments[0] == i)[0]
#     cell_facilities = np.where(grid_assignments[1] == i)[0]

#     print(i, cell_customers, cell_facilities)

#     # Matriz de distancias
#     cell_distances = cdist(customers_coordenates[cell_customers], facilities_coordenates[cell_facilities])

#     # Modelo de programación lineal
#     prob = LpProblem("Capacitated_Facility_Location_Cell_" + str(i), LpMinimize)

#     # Variables de decisión
#     facility_vars = LpVariable.dicts("Facility", cell_facilities, lowBound=0, cat='Binary')
#     customer_vars = LpVariable.dicts("Customer", cell_customers, lowBound=0, cat='Integer')

#     # Función objetivo
#     prob += lpSum([facility_vars[j] for j in cell_facilities])

#     # Restricción de capacidad de las facilidades
#     for j in cell_facilities:
#         prob += lpSum([customer_demands[k]*customer_vars[k] for k in cell_customers]) <= facility_capacities[j]*facility_vars[j]

#     # Restricción de asignación de clientes a facilidades
#     for k in cell_customers:
#         prob += lpSum([facility_vars[j]*customer_vars[k] for j in cell_facilities]) == customer_vars[k]

#     # Resolver el modelo
#     prob.solve()

#     # Guardar la solución
#     cell_facility_customers = []
#     for j in cell_facilities:
#         cell_facility_customers.append([k for k in cell_customers if customer_vars[k].value() > 0])
#     facility_customers.append(cell_facility_customers)

# # Integración de las soluciones de los subproblemas
# solution = []
# for j in range(facility_count):
#     assigned_customers = []
#     for i in range(len(grid_assignments)):
#         if j in grid_assignments[1][grid_assignments[0] == i]:
#             cell_index = np.where(grid_assignments[1] == j)[0][0]
#             assigned_customers += facility_customers[cell_index][j-grid_assignments[1][grid_assignments[0] == i][0]]
#     solution.append(assigned_customers)

# # Imprimir la solución
# for j, customers in enumerate(solution):
#     if customers:
#         print(f"Facility {j} is serving customers {customers}")