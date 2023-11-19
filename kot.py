import numpy as np

# Example usage
C = [1, 2, 3]  # Set of controllers
V = [1, 2, 3, 4]  # Set of vertices
p = {1: {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4},
     2: {1: 0.4, 2: 0.3, 3: 0.2, 4: 0.1},
     3: {1: 0.2, 2: 0.1, 3: 0.4, 4: 0.3}}  # Probability matrix
alpha = np.zeros((len(C), len(V)))

# Populate alpha matrix
for i, controller in enumerate(C):
    for j, vertex in enumerate(V):
        alpha[i, j] = np.log(1 - p[controller][vertex])
print(alpha)