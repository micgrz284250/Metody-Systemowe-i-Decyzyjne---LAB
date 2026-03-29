"""Module for parsing problem data from DIMACS file format"""

import networkx as nx

# from models.graph import Graph

_PROBLEM_TYPE = "edge"

# Od tych znaków zaczyna się każda linia
_COMMENT_INDICATOR = "c"
_PROBLEM_INDICATOR = "p"
_EDGE_INDICATOR = "e"


# Prawdopodobnie niepotrzebne, do usunięcia gdy nie będzie konieczności zostawienia
#def parse_problem_data_text_to_graph(file_name: str) -> Graph:
    #"""Function returning a Graph object from DIMACS problem file"""
    #with open(file_name, "r", encoding="utf-8") as file :
        #no_nodes, no_edges = 0, 0
        #neighbour_sets = []
        #for full_line in file:
            #if line := full_line.strip():
                #data = line.split()
                #command_type_indicator = data[0]
                #if command_type_indicator == _PROBLEM_INDICATOR:
                    #[_, problem_type, no_nodes, no_edges] = data
                    #if problem_type != _PROBLEM_TYPE:
                        #raise ValueError(f'Problem type should be "{_PROBLEM_TYPE}"')
                    #neighbour_sets = [{} for _ in range(no_nodes)]
                #elif command_type_indicator == _EDGE_INDICATOR:
                    #[_, fst_verticle, sec_verticle] = data
                    #if not neighbour_sets:
                        #raise ValueError(
                            #"Problem data not set. Please set number of nodes"
                        #)
                    #fst_verticle_idx = fst_verticle - 1
                    #sec_verticle_idx = sec_verticle - 1
                    #neighbour_sets[fst_verticle_idx].add(sec_verticle_idx)
                    #neighbour_sets[sec_verticle_idx].add(fst_verticle_idx)
                #elif command_type_indicator != _COMMENT_INDICATOR:
                    #raise ValueError(f'Unknown operation "{command_type_indicator}"')
        #neighbour_lists = [list(neighbour_set) for neighbour_set in neighbour_sets]
        ## Zaczynamy od braku kolorów (żaden wierzchołek nie jest pokolorowany)
        #colors_list = [None for _ in range(no_nodes)]
        #return Graph(no_nodes, no_edges, neighbour_lists, colors_list)


def parse_problem_data_text_to_nx_graph(file_name: str) -> nx.Graph:
    """Function returning a nx.Graph object from DIMACS problem file"""
    with open(file_name, "r", encoding="utf-8") as file :
        graph = nx.Graph()
        for full_line in file:
            if line := full_line.strip():
                data = line.split()
                command_type_indicator = data[0]
                if command_type_indicator == _PROBLEM_INDICATOR:
                    [_, problem_type, _, _] = data
                    if problem_type != _PROBLEM_TYPE:
                        raise ValueError(f'Problem type should be "{_PROBLEM_TYPE}"')
                elif command_type_indicator == _EDGE_INDICATOR:
                    [_, fst_verticle, sec_verticle] = data
                    graph.add_edge(fst_verticle, sec_verticle)
                elif command_type_indicator != _COMMENT_INDICATOR:
                    raise ValueError(f'Unknown operation "{command_type_indicator}"')
        return graph

def parse_problem_data_binary_to_nx_graph(file_name: str):
    """TODO parse binary DIMACS file"""
    pass
