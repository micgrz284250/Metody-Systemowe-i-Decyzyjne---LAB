from math import inf

import networkx as nx


def evaluate(graph: nx.Graph, colors: dict[int, int]) -> float:
    if graph.number_of_nodes() != len(colors):
        raise ValueError('Graph and colors mismatch')

    for node in graph.nodes:
        adjacent = graph.neighbors(node)
        for neighbor in adjacent:
            if colors[int(node)] == colors[int(neighbor)]:
                return inf
    return (max(colors.values()) - min(colors.values())) + 1