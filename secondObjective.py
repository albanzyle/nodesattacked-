from pulp import LpProblem, LpVariable, lpSum, LpMinimize,LpMaximize, LpStatus, log
import numpy as np
import math
from decimal import Decimal
def solve_linear_problem2(N, M, K, pij,lambda2,indexj,indexi):

    # Create the LP problem
    problem = LpProblem("Linear_Problem", LpMinimize)

    # Define the decision variables
    x = LpVariable.dicts("x", N, lowBound=0, upBound=1, cat="Binary")
    lambda1 = LpVariable("lambda1")

    # Add the objective function
    problem += lambda1
    # Add the constraints
    for j in M:
        if j in indexj:
            continue
        problem += lpSum(math.log(1 - pij[i][j]) * x[i] for i in N) <= lambda1
        
    l=0

    for j in indexj:
            problem += lpSum([math.log(1 - pij[i][j]) * x[i] for i in N]) == lambda2[l]
            l+=1
    

    problem += lpSum(x[i] for i in N) == K
    # Initialize a variable to store the optimal j value
    optimal_j = None

    # Solve the problem
    problem.solve()
    # l=0
    # for j in indexj:
    #    print("this is the lambda that should ccorrospond to that index:",lambda2[l])
    #    print("this is the indexxxxxxxxxxxxxxxx:",j)
    #    l+=1

    # Iterate over the constraints to find the corresponding j value
    for j in M:
        if j in indexj:
            continue        
        # print(f"Value for this {j} = ", sum(math.log(1 - pij[i][j]) * x[i].varValue for i in N))
        # print("lambda1 value ", lambda1.varValue)
        # Convert lambda1.varValue to a Decimal object
        lambda1_decimal = Decimal(str(lambda1.varValue))    
        # Convert the decimal number to a tuple representation
        decimal_tuple = lambda1_decimal.as_tuple()

        # Count the number of digits after the decimal point
        num_digits_after_decimal = abs(decimal_tuple.exponent)
        trimmed_number = round(sum(math.log(1 - pij[i][j]) * x[i].varValue for i in N), num_digits_after_decimal)
        # if optimal_j != None:
        #     continue
        if trimmed_number == lambda1.varValue:
            optimal_j = j
            # break
    lambda_optimal = sum(math.log(1 - pij[i][optimal_j]) * x[i].varValue for i in N)
    # Return the optimal solution and the corresponding j value
    optimal_solution = {
        "lambda1": lambda_optimal,
        "optimal_j": optimal_j,
        "x": [x[i].varValue for i in N]
    }

    # print("lambdaaaaaaaaaaa", lambda2)
    # print("indexxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", indexj)
    # print("Optimal Solution for iteration:", indexi)
    # print("lambda =", lambda1.varValue)
    # print("Optimal j =", optimal_j)
    # controllers = []
    # for i in N:
    #     if x[i].varValue == 1:
    #         j=i
    #         controllers.append(j+1)

    # print("Controllers:",controllers)
    return optimal_solution



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