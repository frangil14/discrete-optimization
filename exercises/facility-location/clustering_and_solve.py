import numpy as np
import pandas as pd
from pulp import *
from utils import length


file = 'fl_100_1'
grid_size = 80000

full_path = os.path.realpath(__file__)
filename = os.path.join('data',file)
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

# Dividimos el plano en grillas
facility_df['col'] = np.floor(facility_df['x_coor'] / grid_size).astype(int)
facility_df['row'] = np.floor(facility_df['y_coor'] / grid_size).astype(int)

customer_df['col'] = np.floor(customer_df['x_coor'] / grid_size).astype(int)
customer_df['row'] = np.floor(customer_df['y_coor'] / grid_size).astype(int)

max_number_columns = max(facility_df['col'].max(),customer_df['col'].max())
max_number_rows = max(facility_df['row'].max(),customer_df['row'].max())


statuses = []
facility_customers = []
facility_customers_original_index = []
costs = []
# Iterar sobre las regiones
for columna in range(max_number_columns+1):
    for fila in range(max_number_rows+1):
    # Seleccionar clientes y facilidades de la celda i, j
        cell_customers = customer_df[
            (customer_df["row"] == fila) &
            (customer_df['col'] == columna) ]

        cell_facilities = facility_df[
            (facility_df["row"] == fila) &
            (facility_df['col'] == columna) ]
        
        
        # Matriz de distancias
        customer_facility_distances = [[length(c['x_coor'], c['y_coor'], f['x_coor'], f['y_coor']) for index, c in cell_facilities.iterrows()] for index, f in cell_customers.iterrows()]


        # Define el problema de optimización
        prob = LpProblem("Facility_Location_Problem", LpMinimize)

        num_facilities = cell_facilities.shape[0]
        num_customers = cell_customers.shape[0]

        # Define las variables de decisión
        facility_vars = LpVariable.dicts("Facility", range(num_facilities), lowBound=0, cat='Binary')
        assignment_vars = LpVariable.dicts("Assignment", [(i,j) for i in range(num_customers) for j in range(num_facilities)], lowBound=0, cat='Binary')

        facility_costs = [row['setup_cost'] for index, row in cell_facilities.iterrows()]
        customer_demands = [row['demand'] for index, row in cell_customers.iterrows()]
        facility_capacities = [row['capacity'] for index, row in cell_facilities.iterrows()]

        # Define la función objetivo
        prob += lpSum([facility_costs[j]*facility_vars[j] for j in range(num_facilities)] + [customer_facility_distances[i][j]*assignment_vars[(i,j)] for i in range(num_customers) for j in range(num_facilities)])

        # Define las restricciones
        for i in range(num_customers):
            prob += lpSum([assignment_vars[(i,j)] for j in range(num_facilities)]) == 1

        for j in range(num_facilities):
            prob += lpSum([assignment_vars[(i,j)]*customer_demands[i] for i in range(num_customers)]) <= facility_capacities[j]*facility_vars[j]


        # # NUEVAS REESTRICCIONES
        # for j in range(num_facilities):
        #     prob += lpSum(assignment_vars[(i,j)] for i in range(num_customers)) <= facility_capacities[j]

        # # Restricción de selección
        # prob += lpSum(facility_vars[j] for j in range(num_facilities)) <= num_facilities

        # Resolver el modelo
        prob.solve()

        final_solution = {}
        final_solution_original_index = {}
        errores = []

        cell_customers = [int(row['index']) for index, row in cell_customers.iterrows()]
        cell_facilities = [int(row['index']) for index, row in cell_facilities.iterrows()]

        for j in range(num_facilities):
            if facility_vars[j].varValue > 0:
                # print("Facilidad %s está abierta." % j)
                clientes_demand = []
                clientes = []
                clientes_original_index = []
                for i in range(num_customers):
                    if assignment_vars[(i,j)].varValue > 0:
                        # print("- Cliente %s está asignado a la facilidad %s." % (i,j))
                        clientes_demand.append(customer_demands[i])
                        clientes.append(i)
                        clientes_original_index.append(cell_customers[i])
                final_solution[j] = clientes

                final_solution_original_index[cell_facilities[j]] = clientes_original_index
                if sum(clientes_demand) > facility_capacities[j]:
                    print('------------------FATAL ERROR-----------------------', j)
                    errores.append((sum(clientes_demand), facility_capacities[j]))

        # Guardar la solución
        costs.append(prob.objective.value())
        statuses.append((fila, columna, LpStatus[prob.status], errores))
        facility_customers.append(final_solution)
        facility_customers_original_index.append(final_solution_original_index)



# prepare the solution in the specified output format

output = {}

for solutions in facility_customers_original_index:
    for key, value in solutions.items():
        for item in value:
            output[item] = key

a = dict(sorted(output.items()))
# print(a)
output = a.values()
a = list(output)
output = []

for item in a:
    output.append(item)

cost = sum(costs)

output_data = '%.2f' %cost  + ' ' + str(0) + '\n'
output_data += ' '.join(map(str, output))

file = open(f"{file}_result.txt", "a")
a = file.write(output_data)
file.close()