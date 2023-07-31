import gurobipy as gp
from gurobipy import GRB
from typing import List


def print_route_and_costs(distance_matrix, routes):
    for i, route in enumerate(routes):
        vehicle = i + 1
        cost = sum(distance_matrix[route[k-1]][route[k]] for k in range(1, len(route)))
        print(f"Vehicle {vehicle} - Route: {route}, Cost: {cost}")


def solve_minmax_vrp(distance_matrix: List[List[int]], vehicle_capacity: int, num_vehicles: int) -> List[List[int]]:
    model = gp.Model("MinmaxVRP")

    # Variables
    x = {}  # Binary variable indicating if node i is visited by vehicle j
    for i in range(len(distance_matrix)):
        for j in range(num_vehicles):
            x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    y = model.addVar(vtype=GRB.CONTINUOUS, name="y")  # Maximum cost among all vehicles

    # Set objective
    model.setObjective(y, GRB.MINIMIZE)

    # Constraints
    for i in range(len(distance_matrix)):
        model.addConstr(gp.quicksum(x[i, j] for j in range(num_vehicles)) == 1, f"visit_once_{i}")

    for j in range(num_vehicles):
        model.addConstr(gp.quicksum(x[i, j] for i in range(len(distance_matrix))) <= vehicle_capacity, f"capacity_{j}")

    for j in range(num_vehicles):
        model.addConstr(y >= gp.quicksum(distance_matrix[i][k] * x[i, j] for i in range(len(distance_matrix)) for k in range(len(distance_matrix)) if k != i), f"route_cost_{j}")

    # Optimize the model
    model.optimize()

    # Extract the routes
    routes = [[] for _ in range(num_vehicles)]
    for i, j in x.keys():
        if x[i, j].X > 0.5:  # Node i is visited by vehicle j
            routes[j].append(i)

    return routes


def solve_minsum_vrp(distance_matrix: List[List[int]], vehicle_capacity: int, num_vehicles: int) -> List[List[int]]:
    model = gp.Model("MinsumVRP")

    # Variables
    x = {}  # Binary variable indicating if node i is visited by vehicle j
    for i in range(len(distance_matrix)):
        for j in range(num_vehicles):
            x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    # Set objective
    model.setObjective(gp.quicksum(distance_matrix[i][j] * x[i, j] for i in range(len(distance_matrix))
                                  for j in range(num_vehicles)), GRB.MINIMIZE)

    # Constraints
    for i in range(len(distance_matrix)):
        model.addConstr(gp.quicksum(x[i, j] for j in range(num_vehicles)) == 1, f"visit_once_{i}")

    for j in range(num_vehicles):
        model.addConstr(gp.quicksum(x[i, j] for i in range(len(distance_matrix))) <= vehicle_capacity, f"capacity_{j}")

    # Optimize the model
    model.optimize()

    # Extract the routes
    routes = [[] for _ in range(num_vehicles)]
    for i, j in x.keys():
        if x[i, j].X > 0.5:  # Node i is visited by vehicle j
            routes[j].append(i)

    return routes
