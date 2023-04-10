import math
from pulp import value

def get_linked_customers(input_warehouse, served_customer):
    '''
    Find customer ids that are served by the input warehouse.
    
    Args:
        - input_warehouse: string (example: <Warehouse 21>)
    Out:
        - List of customers ids connected to the warehouse
    '''
    # Initialize empty list
    linked_customers = []
    
    # Iterate through the xij decision variable
    for (k, v) in served_customer.items():
            
            # Filter the input warehouse and positive variable values
            if k[1]==input_warehouse and value(v)>0:
                
                # Customer is served by the input warehouse
                linked_customers.append(k[0])

    return linked_customers


def length(point1_xcoor, point1_ycoor, point2_xcoor, point2_ycoor):
    return math.sqrt((point1_xcoor - point2_xcoor)**2 + (point1_ycoor - point2_ycoor)**2)