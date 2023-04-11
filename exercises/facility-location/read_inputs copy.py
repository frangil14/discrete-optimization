from pulp import *

# Define los datos del problema
num_customers = 5
num_facilities = 2
customer_demands = [10, 20, 30, 40, 50]
facility_capacities = [100, 200]
facility_costs = [100, 200]
customer_facility_distances = [[5, 10], [7, 12], [8, 11], [6, 14], [9, 13]]

# Define el problema de optimización
prob = LpProblem("Facility_Location_Problem", LpMinimize)

# Define las variables de decisión
facility_vars = LpVariable.dicts("Facility", range(num_facilities), lowBound=0, cat='Binary')
assignment_vars = LpVariable.dicts("Assignment", [(i,j) for i in range(num_customers) for j in range(num_facilities)], lowBound=0, cat='Binary')

# Define la función objetivo
prob += lpSum([facility_costs[j]*facility_vars[j] for j in range(num_facilities)] + [customer_facility_distances[i][j]*assignment_vars[(i,j)] for i in range(num_customers) for j in range(num_facilities)])

# Define las restricciones
for i in range(num_customers):
    prob += lpSum([assignment_vars[(i,j)] for j in range(num_facilities)]) == 1

for j in range(num_facilities):
    prob += lpSum([assignment_vars[(i,j)]*customer_demands[i] for i in range(num_customers)]) <= facility_capacities[j]*facility_vars[j]

# Resuelve el problema de optimización
prob.solve()

# Imprime la solución
print("Status: ", LpStatus[prob.status])
print("Costo total: ", value(prob.objective))
for j in range(num_facilities):
    if facility_vars[j].varValue > 0:
        print("Facilidad %s está abierta." % j)
        for i in range(num_customers):
            if assignment_vars[(i,j)].varValue > 0:
                print("- Cliente %s está asignado a la facilidad %s." % (i,j))