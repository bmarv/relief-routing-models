import pandas as pd

from api import carthography, routing

def route_directional_with_ors(
    start_coords: list, 
    end_coords: list,
    profile: str = 'driving-car',
    client: routing.ors.Client = None,
): 
    route = routing.get_directions_ors_py(
        start_coords= start_coords,
        end_coords= end_coords,
        profile= profile,
        client= client
    )

    steps_list = route['features'][0]['properties']['segments'][0]['steps']
    steps_df = pd.DataFrame(steps_list)
    return route, steps_df

def display_directional_route_map(
    route: dict
) -> carthography.folium.Map:
    map_object = carthography.map_rectangular_area(
        bbox= route['features'][0]['bbox'],
    )

    map_object, _poly_line = carthography.map_route(
        locations= route['features'][0]['geometry']['coordinates'],
        map_object= map_object
    )
    return map_object

def route_directional_as_round_trip(
    coordinates: list,
    indices: list,
    profile: str = 'driving-hgv'
):         
    route_list = []
    route_summary_list = []
    client = routing.get_client_ors()
    for step_index in range (1, len(indices)):
        print(f'\tnode {indices[step_index-1]}: {coordinates[step_index-1]} \t| node {indices[step_index]}: {coordinates[step_index]}')

        route, _route_df = route_directional_with_ors(
            start_coords=coordinates[step_index-1],
            end_coords=coordinates[step_index],
            profile= profile,
            client= client
        )
        route_list.append(route)
        route_summary_list.append({
            'index': indices[step_index],
            'distance': route['features'][0]['properties']['segments'][0]['distance'],
            'duration': route['features'][0]['properties']['segments'][0]['duration'],
        })

    return route_list, pd.DataFrame(route_summary_list)

def display_directional_route_round_trip_on_map(
    route_list: list,
    coordinates: list,
    indices: list
):
    map_object = carthography.map_rectangular_area(
        bbox= route_list[0]['features'][0]['bbox'],
        zoom_start=15
    )
    for idx, el in enumerate(route_list):
        # map sub-route
        map_object, _poly_line = carthography.map_route(
            locations= route_list[idx]['features'][0]['geometry']['coordinates'],
            map_object= map_object
        )
        # map marker with indices
        map_object = carthography.add_marker_to_map(
            map_object= map_object,
            coordinates= coordinates[idx],
            text= indices[idx]
        )

    return map_object