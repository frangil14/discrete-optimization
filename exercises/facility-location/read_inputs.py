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

    annual_supply_dict = { 'Warehouse ' + str(warehouse[0]) : warehouse[2] for warehouse in facilities }

    # Dictionary of warehouse id (id) and fixed costs (value)
    annual_cost_dict = { 'Warehouse ' + str(warehouse[0]) : warehouse[1] for warehouse in facilities }


    # Dict to store the distances between all warehouses and customers
    transport_costs_dict = {}
    demand_dict = { customer : customer_df['demand'][i] for i, customer in enumerate(customer_df['customer_id']) }


    # For each warehouse location
    for i in range(0, facility_df.shape[0]):
        
        # Dict to store the distances between the i-th warehouse and all customers
        warehouse_transport_costs_dict = {}
        
        # For each customer location
        for j in range(0, customer_df.shape[0]):
            
            # Distance in Km between warehouse i and customer j
            d = length(facility_df.x_coor[i],facility_df.y_coor[i],customer_df.x_coor[j],customer_df.y_coor[j])
            
            # Update costs for warehouse i
            warehouse_transport_costs_dict.update({customer_df.customer_id[j]: d})
        
        # Final dictionary with all costs for all warehouses
        transport_costs_dict.update({facility_df.warehouse_id[i]: warehouse_transport_costs_dict})

    # Define linear problem
    lp_problem = LpProblem('Capacitated Facility Location Problem', LpMinimize)


    # Variable: y_j (constraint: it is binary)
    created_facility = LpVariable.dicts(
        'Create_facility', facility_df['warehouse_id'], 0, 1, LpBinary)

    # Variable: x_ij
    served_customer = LpVariable.dicts(
        'Link', [(i,j) for i in customer_df['customer_id'] for j in facility_df['warehouse_id']], 0)


    # Objective function 
    objective = lpSum(annual_cost_dict[j]*created_facility[j] for j in facility_df['warehouse_id']) +\
                lpSum(transport_costs_dict[j][i]*served_customer[(i,j)] \
                    for j in facility_df['warehouse_id'] for i in customer_df['customer_id'])

    lp_problem += objective

    # Costraint: the demand must be met
    for i in customer_df['customer_id']:
        lp_problem += lpSum(served_customer[(i,j)] for j in facility_df['warehouse_id']) == demand_dict[i]

    # Constraint: a warehouse cannot deliver more than its capacity limit
    for j in facility_df['warehouse_id']:
        lp_problem += lpSum(served_customer[(i,j)] for i in customer_df['customer_id']) <= annual_supply_dict[j] * created_facility[j]

    # Constraint: a warehouse cannot give a customer more than its demand
    for i in customer_df['customer_id']:
        for j in facility_df['warehouse_id']:
            lp_problem += served_customer[(i,j)] <= demand_dict[i] * created_facility[j]

    resultado = lp_problem.solve()
    print(resultado)
    # lp_problem.solve(GLPK(msg = 0))


    print('Solution: ', LpStatus[lp_problem.status])

    # List of the values assumed by the binary variable created_facility
    facility_values = [i.varValue for i in created_facility.values()]

    # Count of each distinct value of the list
    [[i, facility_values.count(i)] for i in set(facility_values)]

    # Create dataframe column to store whether to build the warehouse or not 
    facility_df['build_warehouse'] = ''

    # Assign Yes/No to the dataframe column based on the optimization binary variable
    for i in facility_df['warehouse_id']:
        if created_facility[i].varValue == 1:
            facility_df.loc[facility_df['warehouse_id'] == i, 'build_warehouse'] = 'Yes'
        else:
            facility_df.loc[facility_df['warehouse_id'] == i, 'build_warehouse'] = 'No'

    if plot == True:
        colors = ['#990000', '#0059b3']

        facility_df.build_warehouse.value_counts().plot.barh(
        title='Warehouse sites to be established', xlabel='Number of sites', color=colors, ylabel='Establish', figsize=(7,6)) 

        for i, v in enumerate(facility_df.build_warehouse.value_counts()):
            plt.text(v, i, ' '+str(round(v,3)), color=colors[i], va='center', fontweight='bold')

        plt.show()


    facility_df_build = facility_df[facility_df['build_warehouse']=='Yes']
    facility_df_notbuild = facility_df[facility_df['build_warehouse']=='No']

    if plot == True:

        plt.scatter(x = facility_df_build['x_coor'], y = facility_df_build['y_coor'],
                    marker='o', c='#0059b3',  label='Build')
        plt.scatter(x = facility_df_notbuild['x_coor'], y = facility_df_notbuild['y_coor'],
                    marker='X', c='#990000',  label='Discard')


        # Add title
        plt.title('Optimized Warehouse Sites')

        # Add legend
        plt.legend(title='Warehouse Site', facecolor='white')

        # Remove ticks from axis
        plt.xticks([])
        plt.yticks([])

        # Show plot
        plt.show()

    # Warehouses to establish
    establish = facility_df.loc[facility_df.build_warehouse =='Yes']   

    if plot == True:

        plt.scatter(x = establish['x_coor'], y = establish['y_coor'],
                    marker='o', c='#0059b3',  label='Warehouse')
        plt.scatter(x = customer_df['x_coor'], y = customer_df['y_coor'],
                    marker='X', color='#990000',  alpha=0.8, label='Customer')


    final_solution = {}
    test = {}

    # For each warehouse to build
    for w in establish.warehouse_id:

        # Extract list of customers served by the warehouse

        linked_customers = []
    
        # Iterate through the xij decision variable
        for (k, v) in served_customer.items():
                # if input_warehouse == 'Warehouse 35':
                #     print(k,v, input_warehouse)
                #     print(v.varValue)
                
                # Filter the input warehouse and positive variable values
                if k[1]==w and v.varValue>0:
                    
                    # Customer is served by the input warehouse
                    linked_customers.append(k[0])

        # linked_customers = get_linked_customers(w, served_customer)
        final_solution[w] = linked_customers

        # establish.loc[establish.warehouse_id==w].capacity
        # customer_df.loc[customer_df.customer_id==c].demand
        # For each served customer

        customers_demand = []

        for c in linked_customers:
            
            customers_demand.append(customer_df.loc[customer_df.customer_id==c].demand.values[0])
            # Plot connection between warehouse and the served customer
            plt.plot(
            [establish.loc[establish.warehouse_id==w].x_coor, customer_df.loc[customer_df.customer_id==c].x_coor],
            [establish.loc[establish.warehouse_id==w].y_coor, customer_df.loc[customer_df.customer_id==c].y_coor],
            linewidth=0.8, linestyle='--', color='#0059b3')
        test[w] = (establish.loc[establish.warehouse_id==w].capacity.values[0], customers_demand)

        if sum(customers_demand) > establish.loc[establish.warehouse_id==w].capacity.values[0]:
            print('------------------FATAL ERROR-----------------------', w)

    if plot == True:
        # Add title
        plt.title('Optimized Customers Supply', fontsize = 35)

        # Add legend
        plt.legend(facecolor='white', fontsize=30)

        # Remove ticks from axis
        plt.xticks([])
        plt.yticks([])

        # Show plot
        plt.show()

    output = {}

    for key, value in final_solution.items():
        for item in value:
            output[item] = key


    print(test)

    a = dict(sorted(output.items()))
    # print(a)
    output = a.values()
    a = list(output)
    output = []

    for item in a:
        output.append(int(item.replace('Warehouse ','')))
    
    cost = lp_problem.objective.value()
    
    output_data = '%.2f' %cost  + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, output))
    return output_data