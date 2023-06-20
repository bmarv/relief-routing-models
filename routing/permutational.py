import itertools
import pandas as pd

from api import carthography, routing
from routing import directional

def get_permutations(
    coordinates: list,
    indices: list
) -> list:
    index_sub_permutations = list(itertools.permutations(indices[1:-1]))
    indices_permuted = []
    for el in index_sub_permutations:
        el_list = [i for i in el]
        indices_permuted.append([0]+ el_list+ [0])
    
    coordinates_permuted = []

    for idx, el in enumerate(indices_permuted):
        new_coords = []
        for i in indices_permuted[idx]:
            new_coords.append(coordinates[i])
        coordinates_permuted.append(new_coords)
    return coordinates_permuted, indices_permuted

def route_permutational_with_ors(
    coordinates: list,
    indices: list,
    profile: str = 'driving-hgv'
):
    coordinates_permuted, indices_permuted = get_permutations(
        coordinates= coordinates,
        indices= indices
    )
    permutations_route_list = []

    for idx, el in enumerate(indices_permuted):
        print(f'index: {idx}, indices_permuted: {indices_permuted[idx]}, coords_permuted: {coordinates_permuted[idx]} ')
        route_list, route_sum_df = directional.route_directional_as_round_trip(
            coordinates= coordinates_permuted[idx], 
            indices=indices_permuted[idx],
            profile= profile
        )
        permutations_route_list.append(
            {
                'index': idx,
                'route_list': route_list,
                'route_sum_df': route_sum_df
            }
        )
    return permutations_route_list