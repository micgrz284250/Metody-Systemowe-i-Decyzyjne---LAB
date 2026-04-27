def sort_by_available(graph, nodes, colors: dict[int, int]) -> list[int]:
    return sorted(nodes, reverse=True, key=lambda x: get_uncolored_neighbors_count(graph, x, colors))

def get_uncolored_neighbors_count(graph, node, colors: dict[int, int]) -> int:
    uncolored_nodes = 0
    for neighbor in graph.neighbors(node):
        if colors[neighbor] is None:
            uncolored_nodes += 1
    return uncolored_nodes

def get_uncolored_nodes(graph, colors: dict[int, int]) -> list[int]:
    return [node for node in graph.nodes if colors[node] is None]