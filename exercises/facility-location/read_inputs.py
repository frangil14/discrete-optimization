import pandas as pd
import os
from pulp import LpProblem, LpMinimize, LpVariable, LpBinary, lpSum, LpStatus, value, GLPK
from utils import length

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# def get_linked_customers(input_warehouse):
#     '''
#     Find customer ids that are served by the input warehouse.
    
#     Args:
#         - input_warehouse: string (example: <Warehouse 21>)
#     Out:
#         - List of customers ids connected to the warehouse
#     '''
#     # Initialize empty list
#     linked_customers = []
    
#     # Iterate through the xij decision variable
#     for (k, v) in served_customer.items():
#             # if input_warehouse == 'Warehouse 35':
#             #     print(k,v, input_warehouse)
#             #     print(v.varValue)
            
#             # Filter the input warehouse and positive variable values
#             if k[1]==input_warehouse and v.varValue>0:
                
#                 # Customer is served by the input warehouse
#                 linked_customers.append(k[0])

#     return linked_customers

def get_solution(input_data, plot = False):

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


    if plot == True:

        plt.scatter(x = customer_df['x_coor'], y = customer_df['y_coor'],
                    marker='X', color='red',  alpha=0.5, label='Customer')
        plt.scatter(x = facility_df['x_coor'], y = facility_df['y_coor'],
                    marker='D', color='blue',  alpha=0.5, label='Potential warehouse')
        # Add legend
        plt.legend(facecolor='white', title='Location')

        # Add title
        plt.title('Customer and potential warehouses')

        # Remove ticks from axis
        plt.xticks([])
        plt.yticks([])
        plt.show()



    # Warehouses list
    facility_df['warehouse_id'] = ['Warehouse ' + str(i) for i in range(0, facility_df.shape[0])]
    customer_df['customer_id'] = range(0, customer_df.shape[0])

    # Dictionary of warehouse id (id) and max supply (value)

    facility_capacities = [warehouse[2] for warehouse in facilities]

    # Dictionary of warehouse id (id) and fixed costs (value)
    facility_costs = [warehouse[1] for warehouse in facilities]
    print(facility_costs)


    # Dict to store the distances between all warehouses and customers

    customer_demands = [customer[1] for customer in customers]

    customer_facility_distances = [[length(c[2], c[3], f[3], f[4]) for f in facilities] for c in customers]


    # Define el problema de optimización
    prob = LpProblem("Facility_Location_Problem", LpMinimize)

    num_facilities = facility_df.shape[0]
    num_customers = customer_df.shape[0]

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

    test = {}
    final_solution = {}

    # Imprime la solución
    print("Status: ", LpStatus[prob.status])

    for j in range(num_facilities):
        if facility_vars[j].varValue > 0:
            print("Facilidad %s está abierta." % j)
            clientes_demand = []
            clientes = []
            for i in range(num_customers):
                if assignment_vars[(i,j)].varValue > 0:
                    print("- Cliente %s está asignado a la facilidad %s." % (i,j))
                    clientes_demand.append(customer_demands[i])
                    clientes.append(i)
            final_solution[j] = clientes
            test[j] = (facility_capacities[j], sum(clientes_demand))
            if sum(clientes_demand) > facility_capacities[j]:
                print('------------------FATAL ERROR-----------------------', j)
    print(final_solution)
    output = {}

    for key, value in final_solution.items():
        for item in value:
            output[item] = key


    # print(test)

    a = dict(sorted(output.items()))
    # print(a)
    output = a.values()
    a = list(output)
    output = []

    for item in a:
        output.append(item)
    
    cost = prob.objective.value()
    
    output_data = '%.2f' %cost  + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, output))
    return output_data