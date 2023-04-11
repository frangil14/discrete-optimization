import matplotlib.pyplot as plt
import os
import pandas as pd
plt.style.use('ggplot')

full_path = os.path.realpath(__file__)
filename = os.path.join('data','fl_2000_2')
path = os.path.join(os.path.dirname(full_path), filename)

with open(path, 'r') as input_data_file:
    input_data = input_data_file.read()

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
