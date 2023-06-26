import numpy as np
from matplotlib import pyplot as plt
import pygraphviz
import networkx as nx
from os import path, getcwd


def create_symmetric_adjacency_matrix(matrix):
    matrix_np = np.array(matrix)
    upper = np.triu(matrix_np, k=1)

    # Create the symmetric matrix by mirroring the upper triangle
    distance_bidirectional = upper + upper.T
    return distance_bidirectional


def visualize_graph_from_matrix(
    matrix: list,
    figure_path_relative: str = None
):
    ''' plots a graph with the given nodes and weights to a pdf-file
        arguments:
            * matrix: adjacency matrix declared as a nested list of weights for every node
            * figure_path: string for specifying the path of desire for saving the figure

        @returns the absolute path of the saved figure

        ``` 
        matrix = [
             [0, 10, 5, 10, 5], 
             [14, 0, 7, 20, 7], 
             [10, 14, 0, 14, 10], 
             [7, 20, 7, 0, 14], 
             [5, 10, 5, 10, 0]
         ]
    '''


    multigraph_matrix = nx.from_numpy_array(
         A=np.array(matrix), 
       create_using=nx.MultiGraph
    )

    layout = nx.spring_layout(multigraph_matrix)
    nx.draw(multigraph_matrix, layout, with_labels=True)
    nx.draw_networkx_edge_labels(multigraph_matrix, pos=layout)
    if figure_path_relative is not None:
        file_path_absolute = path.join(getcwd(), figure_path_relative)
        plt.savefig(file_path_absolute)
        return file_path_absolute


def visualize_steps_from_list(
    steps_list: list,
    figure_path_relative: str = None
):
    G = nx.Graph()
    G.add_weighted_edges_from(
        ebunch_to_add= steps_list
    )
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edge_labels(G, pos=pos)
    if figure_path_relative is not None:
        file_path_absolute = path.join(getcwd(), figure_path_relative)
        plt.savefig(file_path_absolute)
        return file_path_absolute