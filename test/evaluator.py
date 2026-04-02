from math import inf

import networkx as nx


def evaluate(graph: nx.Graph, colors: list[int]) -> float:
    if graph.number_of_nodes() != len(colors):
        raise ValueError('Graph and colors mismatch')

    for node in graph.nodes:
        adjacent = graph.neighbors(node)
        for neighbor in adjacent:
            if colors[node] == colors[neighbor]:
                return inf
    if min(colors) == 0:
        return max(colors) + 1
    else:
        return max(colors)