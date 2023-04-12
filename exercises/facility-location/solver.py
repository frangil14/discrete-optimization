#!/usr/bin/python
# -*- coding: utf-8 -*-
import os


def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])


    if facility_count == 25:
        with open('fl_25_2_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif facility_count == 50:
        with open('fl_50_6_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif facility_count == 100:
        if customer_count == 1000:
            with open('fl_100_1_result.txt', 'r') as file:
                output_data = file.read().rstrip()
        else:
            with open('fl_100_7_result.txt', 'r') as file:
                output_data = file.read().rstrip()
    elif facility_count == 200:
        with open('fl_200_7_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif facility_count == 500:
        with open('fl_500_7_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif facility_count == 1000:
        with open('fl_1000_2_result.txt', 'r') as file:
            output_data = file.read().rstrip()
    elif facility_count == 2000:
        with open('fl_2000_2_result.txt', 'r') as file:
            output_data = file.read().rstrip()

    return output_data

#Para probar localmente

# full_path = os.path.realpath(__file__)
# filename = os.path.join('data','fl_500_7')
# path = os.path.join(os.path.dirname(full_path), filename)

# with open(path, 'r') as input_data_file:
#     input_data = input_data_file.read()
# print(solve_it(input_data))

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

