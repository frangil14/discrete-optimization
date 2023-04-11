import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from pulp import *

def assign_to_cells(customers, facilities, cell_size):
    # Define las celdas del plano
    cells = {}
    for c in customers + facilities:
        cell_coords = (int(c[0] // cell_size), int(c[1] // cell_size))
        if cell_coords not in cells:
            cells[cell_coords] = {'customers': [], 'facilities': []}
        if c in customers:
            cells[cell_coords]['customers'].append(c)
        else:
            cells[cell_coords]['facilities'].append(c)
    return cells

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

n_cells = 1

cell_assignments  = assign_to_cells(customers_coordenates, facilities_coordenates, n_cells)


for key, values in cell_assignments.items():
    print(key, values)


# Resolución de subproblemas
facility_customers = []
for i in range(n_cells):
    print(i)
    # Seleccionar clientes y facilidades de la celda i
    cell_customers = np.where(cell_assignments[0] == i)[0]
    cell_facilities = np.where(cell_assignments[1] == i)[0]

    # Matriz de distancias
    cell_distances = cdist(customers_coordenates[cell_customers], facilities_coordenates[cell_facilities])

    # Modelo de programación lineal
    prob = LpProblem("Capacitated_Facility_Location_Cell_" + str(i), LpMinimize)

    # Variables de decisión
    facility_vars = LpVariable.dicts("Facility", cell_facilities, lowBound=0, cat='Binary')
    customer_vars = LpVariable.dicts("Customer", cell_customers, lowBound=0, cat='Integer')

    # Función objetivo
    prob += lpSum([facility_vars[j] for j in cell_facilities])

    # Restricción de capacidad de las facilidades
    for j in cell_facilities:
        prob += lpSum([customer_demands[k]*customer_vars[k] for k in cell_customers]) <= facility_capacities[j]*facility_vars[j]

    # Restricción de asignación de clientes a facilidades
    for k in cell_customers:
        prob += lpSum([facility_vars[j]*customer_vars[k] for j in cell_facilities]) == customer_vars[k]

    # Resolver el modelo
    prob.solve()

    # Guardar la solución
    cell_facility_customers = []
    for j in cell_facilities:
        cell_facility_customers.append([k for k in cell_customers if customer_vars[k].value() > 0])
    facility_customers.append(cell_facility_customers)

# Integración de las soluciones de los subproblemas
solution = []
for j in range(facility_count):
    assigned_customers = []
    for i in range(n_cells):
        if j in cell_assignments[1][cell_assignments[0] == i]:
            cell_index = np.where(cell_assignments[1] == j)[0][0]
            assigned_customers += facility_customers[cell_index][j-cell_assignments[1][cell_assignments[0] == i][0]]
    solution.append(assigned_customers)

# Imprimir la solución
for j, customers in enumerate(solution):
    if customers:
        print(f"Facility {j} is serving customers {customers}")