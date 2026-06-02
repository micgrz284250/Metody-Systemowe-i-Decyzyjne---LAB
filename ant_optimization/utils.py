def sort_by_available(graph, nodes, colors: dict[int, int]) -> list[int]:
    return sorted(nodes, reverse=True, key=lambda x: get_uncolored_neighbors_count(graph, x, colors))


def get_uncolored_neighbors_count(graph, uncolored_nodes, node) -> int:
    neighbors_set = set(graph.neighbors(node))
    return len(neighbors_set & uncolored_nodes)


def get_uncolored_nodes(graph, colors: dict[int, int]) -> set[int]:
    return {node for node in graph.nodes if colors[node] is None}