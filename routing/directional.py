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
