#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from read_inputs import get_solution



def solve_it(input_data):
    output_data = get_solution(input_data)

    file = open(f"fl_2000_2_result.txt", "a")
    a = file.write(output_data)
    file.close()
    # with open('fl_100_7_result.txt', 'r') as file:
    #         output_data = file.read().rstrip()

    return output_data

#Para probar localmente

full_path = os.path.realpath(__file__)
filename = os.path.join('data','fl_2000_2')
path = os.path.join(os.path.dirname(full_path), filename)

with open(path, 'r') as input_data_file:
    input_data = input_data_file.read()
print(solve_it(input_data))

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

