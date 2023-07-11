import numpy as np

def calculate_cost(distance_matrix, route):
    """
    Calculates the total cost of a route based on the given distance matrix.
    """
    cost = 0
    for i in range(len(route) - 1):
        from_node = route[i]
        to_node = route[i + 1]
        cost += distance_matrix[from_node][to_node]
    return cost


def calculate_insertion_cost(distance_matrix, route, position, node):
    """
    Calculates the cost of inserting a node into a route at a specific position
    based on the given distance matrix.
    """
    if position == 0:
        from_node = 0
    else:
        from_node = route[position - 1]
    to_node = route[position] if position < len(route) else 0  # The depot node (node 0)
    insertion_cost = distance_matrix[from_node][node] + distance_matrix[node][to_node] - distance_matrix[from_node][to_node]
    return insertion_cost


def print_route_and_costs(distance_matrix, routes):
    # Print vehicles and routes
    for i, route in enumerate(routes):
        vehicle = i + 1
        cost = calculate_cost(distance_matrix, [0] + route + [0])
        print(f"Vehicle {vehicle} - Route: [0]", end=" -> ")
        for node in route:
            print(f"Node {node}", end=" -> ")
        print("[0], Cost:", cost)


def minsum_insertion_algorithm_feasibility(distance_matrix: np.array, demands: np.array, vehicle_capacity: int, num_vehicles: int, infeasible_nodes: dict):
    '''
    distance_matrix: np.array 2d
    demands: list 1d
    vehicle_capacity: int
    num_vehicles: int
    infeasible_nodes: dict(key: node int, value: list of nodes as int)
    '''
    num_nodes = len(distance_matrix)
    num_routes = min(num_vehicles, num_nodes - 1)  # Excluding the depot (node 0)

    # Initialize the routes and their current loads
    routes = [[] for _ in range(num_routes)]
    loads = [0] * num_routes

    # Sort the nodes by their demand in descending order
    sorted_nodes = sorted(range(1, num_nodes), key=lambda x: demands[x], reverse=True)

    for node in sorted_nodes:
        best_cost = float('inf')
        best_vehicle = -1
        best_position = -1

        # Iterate over all vehicles
        for vehicle in range(num_routes):
            if vehicle in infeasible_nodes and node in infeasible_nodes[vehicle]:
                continue
            # Iterate over all possible positions in the vehicle's route
            for position in range(len(routes[vehicle]) + 1):
                current_load = loads[vehicle] + demands[node]
                if current_load > vehicle_capacity:
                    continue

                # Calculate the cost of inserting the node at the position
                insertion_cost = calculate_insertion_cost(distance_matrix, routes[vehicle], position, node)

                # Update the best cost, vehicle, and position if the cost is lower
                if insertion_cost < best_cost:
                    best_cost = insertion_cost
                    best_vehicle = vehicle
                    best_position = position

        # Insert the node into the best vehicle and position
        if best_vehicle != -1: 
            routes[best_vehicle].insert(best_position, node)
            loads[best_vehicle] += demands[node]

    return routes

def minsum_insertion_algorithm_deadlines(distance_matrix, demands, vehicle_capacity, num_vehicles, deadlines):
    '''
    distance_matrix: np.array 2d
    demands: list 1d
    vehicle_capacity: int
    num_vehicles: int
    deadlines: dict(key: node int, value: deadline int)
    '''
    num_nodes = len(distance_matrix)
    num_routes = min(num_vehicles, num_nodes - 1)  # Excluding the depot (node 0)

    # Initialize the routes and their current loads
    routes = [[] for _ in range(num_routes)]
    loads = [0] * num_routes
    costs = [[] for _ in range(num_routes)]

    # Sort the nodes based on their deadlines (lower deadlines are prioritized)
    sorted_nodes = sorted(range(1, num_nodes), key=lambda x: deadlines[x] or float('inf'))

    for node in sorted_nodes:
        best_cost = float('inf')
        best_vehicle = -1
        best_position = -1

        # Iterate over all vehicles
        for vehicle in range(num_routes):
            # Check if the node's deadline can be fulfilled
            current_cost = calculate_cost(distance_matrix, [0] + routes[vehicle] + [0])
            if deadlines[node] is not None and current_cost + calculate_insertion_cost(distance_matrix, routes[vehicle], len(routes[vehicle]), node) > deadlines[node]:
                continue

            # Initialize the insertion cost for the current vehicle
            insertion_cost = float('inf')

            # Iterate over all possible positions in the vehicle's route
            for position in range(len(routes[vehicle]) + 1):
                current_load = loads[vehicle] + demands[node]
                if current_load > vehicle_capacity:
                    continue

                # Calculate the cost of inserting the node at the position
                current_insertion_cost = calculate_insertion_cost(distance_matrix, routes[vehicle], position, node)

                # Update the insertion cost if the cost is lower
                if current_insertion_cost < insertion_cost:
                    insertion_cost = current_insertion_cost
                    best_vehicle = vehicle
                    best_position = position

            # Update the best cost, vehicle, and position if the cost is lower
            if insertion_cost < best_cost:
                best_cost = insertion_cost
                best_vehicle = vehicle
                best_position = position

        # Insert the node into the best vehicle and position
        routes[best_vehicle].insert(best_position, node)
        loads[best_vehicle] += demands[node]
        costs[best_vehicle].append(best_cost)

    return routes, costs


def minsum_insertion_algorithm_feasibilities_deadlines(distance_matrix, demands, vehicle_capacity, num_vehicles, deadlines, infeasible_nodes):
    '''
    distance_matrix: np.array 2d
    demands: list 1d
    vehicle_capacity: int
    num_vehicles: int
    deadlines: dict(key: node int, value: deadline int)
    infeasible_nodes: dict(key: node int, value: list of nodes as int)
    '''
    num_nodes = len(distance_matrix)
    num_routes = min(num_vehicles, num_nodes - 1)  # Excluding the depot (node 0)

    # Initialize the routes and their current loads
    routes = [[] for _ in range(num_routes)]
    loads = [0] * num_routes
    costs = [[] for _ in range(num_routes)]

    # Sort the nodes based on their deadlines (lower deadlines are prioritized)
    sorted_nodes = sorted(range(1, num_nodes), key=lambda x: deadlines[x] or float('inf'))

    for node in sorted_nodes:
        best_cost = float('inf')
        best_vehicle = -1
        best_position = -1

        # Iterate over all vehicles
        for vehicle in range(num_routes):
            # Skip the current vehicle if the node is infeasible for it
            if vehicle in infeasible_nodes and node in infeasible_nodes[vehicle]:
                continue

            # Check if the node's deadline can be fulfilled
            current_cost = calculate_cost(distance_matrix, [0] + routes[vehicle] + [0])
            if deadlines[node] is not None and current_cost + calculate_insertion_cost(distance_matrix, routes[vehicle], len(routes[vehicle]), node) > deadlines[node]:
                continue

            # Initialize the insertion cost for the current vehicle
            insertion_cost = float('inf')

            # Iterate over all possible positions in the vehicle's route
            for position in range(len(routes[vehicle]) + 1):
                current_load = loads[vehicle] + demands[node]
                if current_load > vehicle_capacity:
                    continue

                # Calculate the cost of inserting the node at the position
                current_insertion_cost = calculate_insertion_cost(distance_matrix, routes[vehicle], position, node)

                # Update the insertion cost if the cost is lower
                if current_insertion_cost < insertion_cost:
                    insertion_cost = current_insertion_cost
                    best_vehicle = vehicle
                    best_position = position

            # Update the best cost, vehicle, and position if the cost is lower
            if insertion_cost < best_cost:
                best_cost = insertion_cost
                best_vehicle = vehicle
                best_position = position

        # Insert the node into the best vehicle and position
        routes[best_vehicle].insert(best_position, node)
        loads[best_vehicle] += demands[node]
        costs[best_vehicle].append(best_cost)

    return routes, costs