#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight', 'valor_especifico'])

# Definir la función de aptitud como la suma de los valores de los objetos incluidos en la mochila
def aptitud(solucion, items, capacity):
    valor_total = 0
    peso_total = 0
    for i in range(len(solucion)):
        if solucion[i] == 1:
            valor_total += items[i][1]
            peso_total += items[i][2]
    if peso_total > capacity:
        return 0
    else:
        return valor_total
    
def get_peso_mochila(solucion, items):
    peso_total = 0
    for i in range(len(solucion)):
        if solucion[i] == 1:
            peso_total += items[i][2]
    return peso_total


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), int(parts[0]) / int(parts[1])))

    # para 30 items, tuve que iterar * 1000 o incluso *10000 = 60000

    num_generaciones = item_count * 5000
    tamano_poblacion = item_count * 15
    prob_mutacion = 0.2

    print("Cantidad de objetos: ", len(items))


    if len(items) == 30:

        # Para 30 items ejecutamos el algoritmo genetico

        # Generar una población inicial de soluciones aleatorias
        poblacion = []
        for i in range(tamano_poblacion):
            solucion = [random.randint(0, 1) for j in range(len(items))]
            poblacion.append(solucion)


        # Evolucionar la población a través de varias generaciones
        for generacion in range(num_generaciones):

            # Seleccionar dos soluciones aleatorias y realizar un cruce de dos puntos
            seleccionados = []
            for i in range(2):
                competidores = random.sample(poblacion, 5)
                seleccionado = max(competidores, key=lambda x: aptitud(x, items, capacity))
                seleccionados.append(seleccionado)
            hijo1 = seleccionados[0][:len(items)//2] + seleccionados[1][len(items)//2:]
            hijo2 = seleccionados[1][:len(items)//2] + seleccionados[0][len(items)//2:]

            # Realizar una mutación de cambio de bit en cada hijo con una cierta probabilidad
            for i in range(len(hijo1)):
                if random.random() < prob_mutacion:
                    hijo1[i] = 1 - hijo1[i]
                if random.random() < prob_mutacion:
                    hijo2[i] = 1 - hijo2[i]

            # Reemplazar las dos soluciones menos aptas de la población con los dos nuevos hijos
            peores_soluciones = sorted(poblacion, key=lambda x: aptitud(x, items, capacity))[:2]
            poblacion[poblacion.index(peores_soluciones[0])] = hijo1
            poblacion[poblacion.index(peores_soluciones[1])] = hijo2

        # Seleccionar la solución más apta de la población final
        mejor_solucion = max(poblacion, key=lambda x: aptitud(x, items, capacity))

        print("Valor total de la mochila: %d" % aptitud(mejor_solucion, items, capacity))
        print("Peso de la mochila: %d" % get_peso_mochila(mejor_solucion, items))
        print("No me puedo exceder de: %d" % capacity)

        # prepare the solution in the specified output format
        output_data = str(aptitud(mejor_solucion, items, capacity)) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, mejor_solucion))

    else:
        # Para más de 30 items ejecutamos el algoritmo greedy basado en el valor especifico: valor/peso

        items.sort(key=lambda x: x.valor_especifico, reverse=True)
        value = 0
        weight = 0
        taken = [0]*len(items)

        for item in items:
            if weight + item.weight <= capacity:
                taken[item.index] = 1
                value += item.value
                weight += item.weight
    
        # prepare the solution in the specified output format
        output_data = str(value) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, taken))

    return output_data


# Para probar localmente

# full_path = os.path.realpath(__file__)
# filename = os.path.join('data','ks_30_0')
# path = os.path.join(os.path.dirname(full_path), filename)

# with open(path, 'r') as input_data_file:
#     input_data = input_data_file.read()
# print(solve_it(input_data))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
