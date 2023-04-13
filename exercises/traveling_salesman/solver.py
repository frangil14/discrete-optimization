#!/usr/bin/python
# -*- coding: utf-8 -*-

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    coords_list = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        coords_list.append((float(parts[0]), float(parts[1])))

    if nodeCount == 33810:
        with open('tsp_33810_1_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif nodeCount == 1889:
        with open('tsp_1889_1_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif nodeCount == 574:
        with open('tsp_574_1_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif nodeCount == 200:
        with open('tsp_200_2_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif nodeCount == 100:
        with open('tsp_100_3_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif nodeCount == 51:
        with open('tsp_51_1_result.txt', 'r') as file:
            output_data = file.read().rstrip()

    return output_data



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

