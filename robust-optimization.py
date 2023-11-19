import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpStatus, log

def solve_proportional_robust_controller_placement_integral(C, alpha, M, Gamma, V):
    # Create the linear programming problem
    prob = LpProblem("ProportionalRobustControllerPlacement", LpMinimize)

    # Define decision variables
    x = {i: LpVariable(name=f"x_{i}", cat='Binary') for i in C}
    beta = LpVariable(name="beta", lowBound=0)
    delta = {i: LpVariable(name=f"delta_{i}", lowBound=0) for i in C}
    # alpha = {(i, j): LpVariable(name=f"alpha_{i}_{j}", lowBound=0) for i in C for j in V}

    # Additional variables for A_i
    A = {i: lpSum(alpha[i-1, j-1] for j in V) for i in C}

    # # Create variable for Gamma
    # gamma_var = LpVariable(name="Gamma_var", lowBound=0)
    # prob += gamma_var == Gamma  # Link the variable to the input parameter

    # Objective function
    prob += lpSum(A[i] * x[i] for i in C) + Gamma*beta + lpSum(delta[i] for i in C), "Objective"

    # Constraints
    prob += lpSum(x[i] for i in C) == M, "Constraint1"
    for i in C:
        # prob += A[i] == lpSum(alpha[i-1, j-1] for j in V), f"Constraint2_{i}"
        prob += A[i] * x[i] + beta + delta[i] >= 0, f"Constraint3_{i}"
    
    # # Log constants constraints
    # for i in C:
    #     for j in V:
    #         prob += alpha[i-1, j-1] == log(1 - p[i][j]), f"LogConstraint1_{i}_{j}"

    # Solve the problem
    prob.solve()

    # Check the solution status
    if LpStatus[prob.status] == "Optimal":
        # Get the optimal values of decision variables
        optimal_values = {var.name: var.value() for var in prob.variables()}

        # Sort the coefficients and select the first Gamma elements
        # sorted_coefficients = sorted(A.values())
        # selected_coefficients = sorted_coefficients[:int(Gamma)]
        # for i in C:
        #     if A[i] not in selected_coefficients:
        #         optimal_values[f"x_{i}"] = 0  # Set non-selected variables to 0

        return optimal_values
    else:
        return None

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
        
M = 2  # Constraint value
Gamma = 1  # Coefficient for the second term in the objective function

result = solve_proportional_robust_controller_placement_integral(C, alpha, M, Gamma, V)
if result:
    print("Optimal Solution:")
    for var, value in result.items():
        print(f"{var}: {value}")
else:
    print("No optimal solution found.")
