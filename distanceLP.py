from pulp import LpMaximize, LpProblem, lpSum, LpVariable, LpMinimize
import pandas as pd
import math

def haversine(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Define the depot destinations
depots = [
    {'Depot': 'G192', 'Capacity': 600, 'latitudine': 45.3406, 'longitudine': 10.8447},
    {'Depot': 'G474', 'Capacity': 0, 'latitudine': 45.7668, 'longitudine': 12.7971},
    {'Depot': 'G068', 'Capacity': 2380, 'latitudine': 44.4575, 'longitudine': 12.2325},
    {'Depot': 'G982', 'Capacity': 1700, 'latitudine': 45.4645, 'longitudine': 12.2671}
]

# Define your data
data = [
    {'Demand': 8, 'latitudine': 45.6519, 'longitudine': 12.2201},
    {'Demand': 20, 'latitudine': 45.7665, 'longitudine': 12.6111},
    {'Demand': 8, 'latitudine': 45.7272, 'longitudine': 12.1422},
    {'Demand': 35, 'latitudine': 45.5033, 'longitudine': 12.2356},
    {'Demand': 10, 'latitudine': 45.6259, 'longitudine': 12.1649},
    {'Demand': 7, 'latitudine': 45.6519, 'longitudine': 12.2202},
    {'Demand': 15, 'latitudine': 45.4377, 'longitudine': 10.7391},
    {'Demand': 5, 'latitudine': 45.9274, 'longitudine': 12.3815},
    {'Demand': 13, 'latitudine': 45.6788, 'longitudine': 12.1342},
    {'Demand': 7, 'latitudine': 45.781, 'longitudine': 12.8906},
    {'Demand': 14, 'latitudine': 45.7593, 'longitudine': 11.7731},
    {'Demand': 3, 'latitudine': 45.5029, 'longitudine': 12.2913},
    {'Demand': 25, 'latitudine': 45.3694, 'longitudine': 11.0493},
    {'Demand': 12, 'latitudine': 45.6656, 'longitudine': 12.2228},
    {'Demand': 12, 'latitudine': 45.4858, 'longitudine': 12.1221},
    {'Demand': 15, 'latitudine': 45.4243, 'longitudine': 11.9268},
    {'Demand': 6, 'latitudine': 45.5534, 'longitudine': 11.817},
    {'Demand': 15, 'latitudine': 45.4633, 'longitudine': 12.2238},
    {'Demand': 12, 'latitudine': 45.44, 'longitudine': 10.8504},
    {'Demand': 15, 'latitudine': 45.2263, 'longitudine': 11.0182},
    {'Demand': 10, 'latitudine': 45.3835, 'longitudine': 12.038},
    {'Demand': 8, 'latitudine': 45.1914, 'longitudine': 12.2774},
    {'Demand': 22, 'latitudine': 45.5109, 'longitudine': 10.9338},
    {'Demand': 8, 'latitudine': 45.782, 'longitudine': 12.4119},
    {'Demand': 37, 'latitudine': 45.7744, 'longitudine': 12.8245},
    {'Demand': 9, 'latitudine': 45.6226, 'longitudine': 12.5499},
    {'Demand': 9, 'latitudine': 45.4454, 'longitudine': 12.2046},
    {'Demand': 30, 'latitudine': 45.5666, 'longitudine': 12.1719},
    {'Demand': 6, 'latitudine': 45.2731, 'longitudine': 11.0978},
    {'Demand': 8, 'latitudine': 45.8763, 'longitudine': 12.3132},
    {'Demand': 10, 'latitudine': 45.5497, 'longitudine': 12.2947},
    {'Demand': 27, 'latitudine': 45.4419, 'longitudine': 12.0507},
    {'Demand': 10, 'latitudine': 45.446, 'longitudine': 11.0515},
    {'Demand': 12, 'latitudine': 45.3568, 'longitudine': 10.7521},
    {'Demand': 5, 'latitudine': 45.5387, 'longitudine': 12.3016}
]

# Initialize a distance matrix
distance_matrix = []

for node in data:
    distances_to_depots = []
    for depot in depots:
        distance = haversine(node['latitudine'], node['longitudine'], depot['latitudine'], depot['longitudine'])
        distances_to_depots.append(distance)
    distance_matrix.append(distances_to_depots)

# Convert the distance_matrix to a DataFrame
df = pd.DataFrame(distance_matrix)

# Define the file path where you want to save the Excel file
file_path = 'distance_matrix.xlsx'

# Save the DataFrame to an Excel file
df.to_excel(file_path, index=False, header=False)
# Print the distance matrix
# for row in distance_matrix:
#     print(row)
    
# Initialize LP problem
model = LpProblem(name="distance_minimization", sense=LpMinimize)

# Define decision variables
x = {(i, j): LpVariable(name=f"x_{i}_{j}", cat='Binary') for i in range(len(data)) for j in range(len(depots))}

# Define objective function (minimize total distance)
model += lpSum(x[i, j] * distance_matrix[i][j] for i in range(len(data)) for j in range(len(depots)))

# Define constraints
for i in range(len(data)):
    model += lpSum(x[i, j] for j in range(len(depots))) == 1  # Each node must be assigned to exactly one depot

for j in range(len(depots)):
    model += lpSum(x[i, j] * data[i]['Demand'] for i in range(len(data))) <= depots[j]['Capacity'] # Capacity constraint for each depot

# Solve the problem
model.solve()

# Extract the results
node_assignments = {i: [j for j in range(len(depots)) if x[i, j].value() == 1][0] for i in range(len(data))}

# Print the results
# print("Distance matrix:", distance_matrix)

# print("Assigned Depots:", assigned_depots)
# print("Node Assignments:", node_assignments)
connected_nodes = {depot['Depot']: [] for depot in depots}

# Populate the connected_nodes dictionary
for i in range(len(data)):
    assigned_depot = node_assignments[i]  # Get the assigned depot for node i
    depot_key = depots[assigned_depot]['Depot']  # Get the depot key
    connected_nodes[depot_key].append(i)  # Append node i to the list of connected nodes for the corresponding depot

# Print the connected_nodes dictionary
print(connected_nodes)
# Initialize an empty dictionary to store the connected nodes with their demands for each depot
connected_nodes_with_demand = {depot['Depot']: [] for depot in depots}

# Populate the connected_nodes_with_demand dictionary
for i in range(len(data)):
    assigned_depot = node_assignments[i]  # Get the assigned depot for node i
    depot_key = depots[assigned_depot]['Depot']  # Get the depot key
    demand_value = data[i]['Demand']  # Get the demand value for node i
    connected_nodes_with_demand[depot_key].append((i, demand_value))  # Append (node, demand) tuple to the list of connected nodes for the corresponding depot

# Print the connected_nodes_with_demand dictionary
# print(connected_nodes_with_demand)
sum_nodes_with_demand = {}

# Calculate the sum of demands for each depot
for depot, connected_nodes in connected_nodes_with_demand.items():
    sum_demand = sum(demand for node, demand in connected_nodes)
    sum_nodes_with_demand[depot] = sum_demand

# Print the sum_nodes_with_demand dictionary
print(sum_nodes_with_demand)
