import random

# Dummy data
sa_nodes = list(range(1, 10))  # Assume you have 9 nodes
controllers = [1, 3, 5]  # Controllers vector
controllers2 = [2, 3, 5]  # Indexes for controllers2

# Print the dummy data
print("sa_nodes:", sa_nodes)
print("controllers:", controllers)
print("indexes:", controllers2)

# controllers2 = [indexes[i] for i in range(len(controllers))]

# Get common nodes between controllers and controllers2
common_nodes = list(set(controllers) & set(controllers2))
print("common_nodes:", common_nodes)

sa_attack_nodes_500_random = {}
available_nodes = list(set(sa_nodes) - set(controllers) - set(controllers2))
print("available_nodes:", available_nodes)

for i in range(1, 5):  # Assume you have 5 iterations
    random_size = 4
    # Exclude nodes from controllers and controllers2 in the random sample
    random_nodes = set(random.sample(available_nodes, random_size - 2))

    # Add two nodes from the common_nodes list
    random_nodes.update(random.sample(common_nodes, 2))

    sa_attack_nodes_500_random[i] = random_nodes

# Print the result
print("sa_attack_nodes_500_random:", sa_attack_nodes_500_random)
