"""Module for parsing problem data from DIMACS file format"""

import networkx as nx

# from models.graph import Graph

_PROBLEM_TYPE = "edge"

# Od tych znaków zaczyna się każda linia
_COMMENT_INDICATOR = "c"
_PROBLEM_INDICATOR = "p"
_EDGE_INDICATOR = "e"

def parse_problem_data_text_to_nx_graph(file_name: str) -> nx.Graph:
    """Function returning a nx.Graph object from DIMACS problem file"""
    with open(file_name, "r", encoding="utf-8") as file :
        edge_count = 0
        graph = nx.Graph()
        for full_line in file:
            if line := full_line.strip():
                data = line.split()
                command_type_indicator = data[0]
                if command_type_indicator == _PROBLEM_INDICATOR:
                    [_, problem_type, num_of_nodes, num_of_edges] = data
                    if problem_type != _PROBLEM_TYPE:
                        raise ValueError(f'Problem type should be "{_PROBLEM_TYPE}"')
                    for node_id in range(1, int(num_of_nodes)+1):
                        graph.add_node(node_id)
                elif command_type_indicator == _EDGE_INDICATOR:
                    [_, fst_node, sec_node] = data
                    graph.add_edge(fst_node, sec_node)
                    edge_count += 1
                    if edge_count > int(num_of_edges):
                        raise ValueError(f'Edge count should be less or equal to {num_of_edges}')
                elif command_type_indicator != _COMMENT_INDICATOR:
                    raise ValueError(f'Unknown operation "{command_type_indicator}"')
        return graph
