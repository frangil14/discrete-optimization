import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass
import numpy as np
from facility_location.utils import length
import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
import math



def plot_solution(coords_list, solution= None, different_points=[],labels=[0]):
    # Define los colores que quieres utilizar para representar cada etiqueta
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k','C0','C1','C2','C3','C4','C5','C6','C7','C8']
    coords_list_np = np.array(coords_list)

    # Crea la figura y grafica las coordenadas
    plt.figure(figsize=(12, 10))
    plt.scatter(coords_list_np[:, 0], coords_list_np[:, 1], c=[colors[label] for label in labels])

    for i in range(len(coords_list_np)):
        x = coords_list_np[i][0]
        y = coords_list_np[i][1]
        # plt.plot(x, y, 'bo')
        plt.text(x * (1 + 0.01), y * (1 + 0.01) , labels[i], fontsize=12)

    if solution is not None:
        coord_x = [coords_list_np[i][0] for i in solution]
        coord_y = [coords_list_np[i][1] for i in solution]

        plt.plot(coord_x, coord_y)

    if len(different_points)>0:
        different_points_np = np.array(different_points)
        plt.scatter(different_points_np[:, 0], different_points_np[:, 1], c='y')
    # Muestra la figura
    plt.show()

def rounded_capacity_ineq(m, where, vehicle_capacity):
    
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

# function for calculating distance between two pins
def _distance_calculator(_df):
    
    _distance_result = np.zeros((len(_df),len(_df)))
    
    for i in range(len(_df)):
        for j in range(len(_df)):
            
            # calculate distance of all pairs
            _distance = length(_df['x_coor'].iloc[i],_df['y_coor'].iloc[i],
                            _df['x_coor'].iloc[j],_df['y_coor'].iloc[j])
            # append distance to result list
            _distance_result[i][j] = _distance
    
    return _distance_result


# Crear una función de distancia que tenga en cuenta la capacidad
# para el problema vrp_200_16_1, usamos penalty = 1000 y percentage = 0.30
def capacity_distance(point1_xcoor, point1_ycoor, point2_xcoor, point2_ycoor, point1_demand, point2_demand, vehicle_capacity, penalty = 1000, percentage = 0.30):
    distance = math.sqrt((point1_xcoor - point2_xcoor)**2 + (point1_ycoor - point2_ycoor)**2)
    if (point1_demand + point2_demand) > vehicle_capacity*percentage:
        return penalty * 1000 # Penalizar la distancia si la capacidad se supera
    else:
        return distance


# function for calculating distance between two pins having into account the Capacity
def distance_calculator_constrained(df, vehicle_capacity):
    
    _distance_result = np.zeros((len(df),len(df)))
    
    for i in range(len(df)):
        for j in range(len(df)):
            
            # calculate distance of all pairs
            _distance = capacity_distance(df['x_coor'].iloc[i],df['y_coor'].iloc[i],
                            df['x_coor'].iloc[j],df['y_coor'].iloc[j], df['demand'].iloc[i], df['demand'].iloc[j], vehicle_capacity)
            # append distance to result list
            _distance_result[i][j] = _distance
    
    return _distance_result