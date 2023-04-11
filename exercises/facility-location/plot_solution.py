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
