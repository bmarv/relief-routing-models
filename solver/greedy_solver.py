from copy import deepcopy

def greedy_search(adjacency_matrix: list) -> list:
    index_distances_list = []
    index_order = [0]
    chosen_index = 0
    distance_sum = 0
    for iteration in range(0, len(adjacency_matrix)-1):
        # get elements from chosen node
        node_list = deepcopy(adjacency_matrix[chosen_index])
        # set indices from index_order to 'inf'
        for el in index_order:
            node_list[el] = float('inf')

        current_index = deepcopy(chosen_index)
        print('current_index: ', current_index)
        min_value = min(node_list)
        chosen_index = node_list.index(min_value)
        index_order.append(chosen_index)
        distance_sum += min_value
        
        index_distances_list.append(
            (current_index, chosen_index, min_value)
        )

        print('\t\tchosen_index: ', chosen_index)
        print('\t\tindex_order: ', index_order)
        print('\t\tdistance: ', min_value)
        print('\t\tdistance_sum: ', distance_sum)

    return index_distances_list
