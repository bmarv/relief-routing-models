import pandas as pd

from api import carthography, routing

def route_distancial_with_ors(
    coordinates_list: list, 
    metrics: list = ['distance', 'duration'],
    profile: str = 'driving-hgv',
    client: routing.ors.Client = None,
): 
    matrix = routing.get_matrix_ors_py(
        coordinates_list = coordinates_list,
        metrics = metrics,
        profile = profile,
        client= client
    )
    route_summary_dict_list = []
    route_summary_df_list = []
    for step_index in range (1, len(coordinates_list)):
        current_el_indices = []
        current_el_distances = []
        current_el_durations = []
        for index in range(0, len(matrix['sources'])):
            current_el_indices.append(index)
            current_el_distances.append(matrix['distances'][step_index][index])
            current_el_durations.append(matrix['durations'][step_index][index])
        route_summary_dict = {
                'run': step_index,
                'index': current_el_indices,
                'distances': current_el_distances,
                'durations': current_el_durations
        }
        route_summary_dict_list.append(route_summary_dict)
        route_summary_df_list.append(
            pd.DataFrame(route_summary_dict)
        )
        
    return matrix, route_summary_dict_list, route_summary_df_list
