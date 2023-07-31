# Relief Routing Models
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
feasibilities_deadlines = solver.inexact_solver.minsum_insertion_algorithm_feasibilities_deadlines(
    distance_matrix, demands, vehicle_capacity, num_vehicles, deadlines, infeasible_nodes
)
solver.inexact_solver.print_route_and_costs(distance_matrix, feasibilities_deadlines[0])
```

It is also possible to use visualization options offered in the `carthography`-module or `routing.directional.display_directional_route_round_trip_on_map(...)`.
The visualizations are interactive and for the best used in a Jupyter-Notebook. 
Examples are included in the Notebook `routing_demo.ipynb`

Seismic Acitivies can also be sensed by invoking `api.seismic.get_earthquakes_within_start_and_endtime(...)`. For this external API no keys have to be gained. 
