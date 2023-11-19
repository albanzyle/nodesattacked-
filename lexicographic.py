from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpMaximize
import math
from decimal import Decimal
from secondObjective import solve_linear_problem2

def solve_linear_problem(N, M, K, pij):
    # Create the LP problem
    problem = LpProblem("Linear_Problem", LpMinimize)

    # Define the decision variables
    x = LpVariable.dicts("x", N, lowBound=0, upBound=1, cat="Binary")
    lambda1 = LpVariable("lambda1")

    # Add the objective function
    problem += lambda1

    # Add the constraints
    for j in M:
        problem += lpSum(math.log(1 - pij[i][j]) * x[i] for i in N) <= lambda1

    problem += lpSum(x[i] for i in N) == K

    # Initialize a variable to store the optimal j value
    optimal_j = None

    # Solve the problem
    problem.solve()

    # Iterate over the constraints to find the corresponding j value
    for j in M:
        # print("Value for this j = ", j ,sum(math.log(1 - pij[i][j]) * x[i].varValue for i in N))
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
    return optimal_solution

pij = [ [0.9,0.33333333,0.9,0.33333333,0,0.33333333,0,0.33333333],
        [0.33333333,0.9,0.33333333,0,0,0,0,0],
        [0.9,0.33333333, 0.9,0.33333333,0,0.33333333, 0, 0.33333333],
        [0.33333333, 0, 0.33333333, 0.9,        0, 0.33333333,0,0.33333333],
        [0,     0, 0,    0,     0.9,        0,0.33333333, 0.33333333],
        [0.33333333, 0,         0.33333333, 0.33333333,0, 0.9,0,0.33333333],
        [0,0, 0, 0,    0.33333333, 0, 0.9, 0.66666667],
        [0.33333333, 0, 0.33333333, 0.33333333, 0.33333333, 0.33333333,0.66666667 ,0.9]]  # Example pij matrix


length = len(pij[0])
N = list(range(length)) # Set of i values
M = list(range(length)) # Set of j values
K = 2  # Value of K

indexj =[]
lambda1 = []

solution = solve_linear_problem(N, M, K,pij)
lambda1.append(solution["lambda1"])
indexj.append(solution["optimal_j"])

length = len(N)
avarage_connections =[]
for i in range(length-1):
    infoi = solve_linear_problem2(N,M,K,pij,lambda1, indexj,i+2)
    lambda1.append(infoi["lambda1"])
    indexj.append(infoi["optimal_j"])
controllers = [i+1 for i, val in enumerate(infoi["x"]) if val == 1]
print("this are controllersssssss:",controllers)
# Print the solution
print("Optimal Solution:")
print("lambda1 =", infoi["lambda1"])
print("Controllers =", [i+1 for i, val in enumerate(solution["x"]) if val == 1])
print("Optimal j =", solution["optimal_j"])
print("lambda1 =", lambda1)




