from pyclustering.cluster.kmedoids import kmedoids
from python_tsp.heuristics import *
import os
import pandas as pd
from utils import distance_calculator_constrained, plot_solution, _distance_calculator
import warnings
warnings.filterwarnings("ignore")
#This will ignore all DeprecationWarning warnings in your code.
from utils import length

def get_vecino_cercano_con_capacidad(distances_test, customer_demand, vehicle_capacity):
    if len(distances_test) == 0:
        return None
    vecino_cercano = min(distances_test, key=distances_test.get)
    if dict_recluster[vecino_cercano] + customer_demand <= vehicle_capacity:
        return vecino_cercano
    else:
        del distances_test[vecino_cercano]
        return get_vecino_cercano_con_capacidad(distances_test, customer_demand, vehicle_capacity)



file = 'vrp_200_16_1'

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



df = pd.DataFrame (customers, columns = ['index', 'demand', 'x_coor', 'y_coor'])
df_copy = df.copy()

df_copy = df_copy.drop(0)

demanda_total = df_copy['demand'].sum()

# Crear la matriz de distancia con la función de distancia personalizada
distance_matrix = distance_calculator_constrained(df_copy, vehicle_capacity)

# Crear el objeto k-Medoids y ejecutar el algoritmo
kmedoids_instance = kmedoids(distance_matrix, initial_index_medoids=list(range(0,vehicle_count)))
kmedoids_instance.process()

# Obtener los grupos y los medoides
grupos = kmedoids_instance.get_clusters()
medoides = kmedoids_instance.get_medoids()

# Imprimir los resultados
print("Los grupos resultantes son:")
for i, grupo in enumerate(grupos):
    print(f"Grupo {i}: {grupo}")


df_copy['label'] = 0

for i in range(len(grupos)):
    # print(grupos[i])
    for index in grupos[i]:

        df_copy['label'].iloc[index] = i


dict_recluster = {}
for i in range(len(grupos)):

    temp_df = df_copy[
    (df_copy["label"] == i)]

    max_demand = temp_df['demand'].sum()
    if (max_demand>vehicle_capacity):
        print('Problem', i, max_demand, vehicle_capacity)
    else:
        print('Good', i, max_demand, vehicle_capacity)
    dict_recluster[i] = max_demand

dict_recluster = dict(sorted(dict_recluster.items(),key=lambda x:x[1]))

flag = True
# Reasignar clientes para equilibrar la capacidad de los grupos
while flag:
    for group, demand in dict_recluster.items():
        print(group, demand)
        if demand>vehicle_capacity:
            # si estoy excedido
            # Tomar el cliente con la mayor demanda
            customer_demand = df_copy[(df_copy["label"] == group)]['demand'].max()
            customer_index = df_copy[(df_copy["label"] == group) & (df_copy["demand"] == customer_demand)].head(1).index

            # Calcular la distancia a todos los otros grupos
            distances = {}
            for g in dict_recluster:
                if g != group:
                    medoide = medoides[g]
                    medoid_coordenates = (df_copy.iloc[medoides[g]]['x_coor'],df_copy.iloc[medoides[g]]['y_coor'])
                    customer_coordenates = (df_copy.iloc[customer_index]['x_coor'],df_copy.iloc[customer_index]['y_coor'])
                    print(medoid_coordenates)
                    print(customer_coordenates)
                    distances[g] = length(df_copy.iloc[customer_index]['x_coor'],df_copy.iloc[customer_index]['y_coor'], df_copy.iloc[medoides[g]]['x_coor'],df_copy.iloc[medoides[g]]['y_coor'])


            vecino_cercano = get_vecino_cercano_con_capacidad(distances, customer_demand, vehicle_capacity)
            print(vecino_cercano)
            if vecino_cercano is None:
                customer_demand = df_copy[(df_copy["label"] == group)]['demand'].min()
                customer_index = df_copy[(df_copy["label"] == group) & (df_copy["demand"] == customer_demand)].head(1).index
                distances = {}
                for g in dict_recluster:
                    if g != group:
                        medoide = medoides[g]
                        medoid_coordenates = (df_copy.iloc[medoides[g]]['x_coor'],df_copy.iloc[medoides[g]]['y_coor'])
                        print(medoid_coordenates)
                        customer_coordenates = (df_copy.iloc[customer_index]['x_coor'],df_copy.iloc[customer_index]['y_coor'])
                        print(customer_coordenates)
                        distances[g] = length(df_copy.iloc[customer_index]['x_coor'],df_copy.iloc[customer_index]['y_coor'], df_copy.iloc[medoides[g]]['x_coor'],df_copy.iloc[medoides[g]]['y_coor'])
                # print(distances)
                vecino_cercano = get_vecino_cercano_con_capacidad(distances, customer_demand, vehicle_capacity)
                print(demanda_total, vehicle_count, vehicle_capacity)
                print(dict_recluster[vecino_cercano], customer_demand, vehicle_capacity)


            # asigno el nuevo cluster
            df_copy.loc[customer_index,'label'] = vecino_cercano
            new_demand_oldGroup = df_copy[(df_copy["label"] == group)]['demand'].sum()
            new_demand_newGroup = df_copy[(df_copy["label"] == vecino_cercano)]['demand'].sum()

            #update in dict
            dict_recluster[group] = new_demand_oldGroup
            dict_recluster[vecino_cercano] = new_demand_newGroup


            all_good = all(value <= vehicle_capacity for value in dict_recluster.values())

            if all_good:
                print(dict_recluster)
                flag = False



coords_list = [(row['x_coor'],row['y_coor']) for index, row in df_copy.iterrows()]
labels = [int(row['label']) for index, row in df_copy.iterrows()]

# plot_solution(coords_list,labels=labels)


# asignar los clusters finales al dataframe
df_copy['label'] = 0

for i in range(len(df_copy)):
    df_copy['label'].iloc[i] = labels[i]


solutions = {}
for i in range(len(grupos)):

    print(f'Iteration number {i}')
    temp_df = df_copy[
    (df_copy["label"] == i)]

    distance_matrix = _distance_calculator(temp_df)
    temp_df.reset_index(inplace=True)
    print(temp_df)

    permutation0, distance = solve_tsp_simulated_annealing(distance_matrix)
    initial_cost = distance
    final_solution = permutation0

    for j in range(5):

        print(f'Iteration number {j}')
        permutation, distance = solve_tsp_local_search(distance_matrix, x0=permutation0)

        if distance < initial_cost:
            initial_cost = distance
            print(initial_cost)
            final_solution = permutation

    permutation_original_index = []

    for item in final_solution:
        temp = temp_df.iloc[item]['level_0']
        permutation_original_index.append(int(temp))

    solutions[i] = ( permutation_original_index, initial_cost)


cost = 0


for item in list(solutions.values()):
    cost =+ item[1]

# prepare the solution in the specified output format
outputData = '%.2f' % cost + ' ' + str(0) + '\n'

for item in list(solutions.values()):
    outputData += str(0) + ' ' + ' '.join(map(str, item[0])) + ' ' + str(0) + '\n'


print(outputData)
file = open(f"{file}_result.txt", "a")
a = file.write(outputData)
file.close()