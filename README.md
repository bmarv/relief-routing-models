# Relief Routing Models
Relief Routing is a critical area of application for Vehicle Routing Problems (VRP) and the Traveling Salesperson Problem (TSP). This domain serves a crucial role in aiding people in need during natural disasters, which can potentially save lives. The research work delves into different research aspects and proposes a model implementation. It is important to note that several factors must be taken into account when considering relief routing, such as the feasibility of routing vehicles and the constraints surrounding relief efforts. The optimization of possible routes is crucial to ensure that aid is delivered quickly and efficiently and that the maximum number of people are reached in a timely manner. Therefore, it is of importance that the routing of vehicles is carefully planned and executed, taking into account all necessary factors to ensure the best possible outcome. This research project investigates methods for minimizing the sum of arrival times (MinSum) as well as the maximum arrival time (MinMax) while simultaneously considering the feasibility of the dispatch vehicles. Experiments are conducted with respect to the efficiency, equity, and scalability of the inexact and exact implementation. For improving the dispatchers’ experience another emphasis is set on solution visualizations.

https://www.berlin-university-alliance.de/commitments/teaching-learning/sturop/conference/Archiv/conference-2023/programm/session-c3/c3-2/index.html 

## Project structure

```
|
|-API
|   |-Carthography
|   |-Routing
|   |-Seismic
|
|-Experiments
|   |-API-Connections
|   |-Graph
|   |-Routing
|
|-Routing
|   |-Directional
|   |-Distancial
|   |-Permutational
|
|-Solver
|   |-MinSum
|   |-MinMax
|

```
## Installation
This project is build with Python3.10. Necessary packages can be installed using the PyPI-package manager for Python:
```bash
pip install -r requirements.txt
```

## Usage
This project follows a predefined structure, that is visible above. For using this program, it is necessary to create a (free) account for the routing service [Open Route Service ](https://openrouteservice.org/) (ORS) to gain API-Usage rights. 
Afterwards a `.env`-file needs to be created to store the secret api-key of ORS as a string in the following format
```bash
ORS_API_KEY="your-secret-key-string"
```

To operate a solver, it is possible to choose between the exact and the inexact implementation. Please note, that currently only the inexact solver supports Feasibilities and Deadlines for the Capacitated Vehicle Routing Problem using MinMax and MinSum. 
To create an instance, please use a distance-matrix as a 2d-List indicating the distances, the demands as well as the deadlines as a 1d-List as values for every recipient. Feasibility is done by defining a dictionary with the vehicle as an integer key and as a value a list of not feasibile recipients. The number of vehicles and the (unified) vehicle capacity should be overloaded as simple integer values. 

Use the following commands to integrate a solver into your program:
```python
import solver.inexact_solver

# pre-define hyper-parameters distance_matrix, demands, vehicle_capacity, num_vehicles, deadlines, infeasible_nodes

#---
# capacitated minsum implementation using feasibilities and deadlines
feasibilities_deadlines = solver.inexact_solver.minsum_insertion_algorithm_feasibilities_deadlines(
    distance_matrix, demands, vehicle_capacity, num_vehicles, deadlines, infeasible_nodes
)
solver.inexact_solver.print_route_and_costs(distance_matrix, feasibilities_deadlines[0])

#---
# capacitated minmax implementation using feasibilities and deadlines
minmax_feasibilities_deadlines = solver.inexact_solver.minmax_insertion_algorithm_feasibilities_deadlines(
    distance_matrix, demands, vehicle_capacity, num_vehicles, deadlines, infeasible_nodes
)
solver.inexact_solver.print_route_and_costs(distance_matrix, minmax_feasibilities_deadlines)

```

It is also possible to use visualization options offered in the `carthography`-module or `routing.directional.display_directional_route_round_trip_on_map(...)`.
The visualizations are interactive and for the best used in a Jupyter-Notebook. 
Examples are included in the Notebook `demo.ipynb`

Seismic Acitivies can also be sensed by invoking `api.seismic.get_earthquakes_within_start_and_endtime(...)`. For this external API no keys have to be gained. 
