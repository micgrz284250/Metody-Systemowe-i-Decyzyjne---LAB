import networkx as nx
from dataclasses import dataclass


@dataclass(frozen=True)
class Iteration:
    """Simulated annealing iteration result data. This should immutable, don't edit it."""

    graph: nx.Graph # nx graph instance
    result: dict[str, int] # colors for each node
    colors_used: frozenset[int] # all colors used
    cost: int # calculated cost of iteration
    wrongly_colored_nodes: list[str] # list containing wrongly colored nodes

    @classmethod
    def get_nxt_iteration(cls, graph: nx.Graph, coloring: dict[str, int]):
        """This function returns new iteration data based on graph and coloring"""
        from simulated_annealing.simulation import (
            get_wrongly_colored_nodes,
            get_colors_set,
            cost_function,
        )
        wrongly_colored = list(get_wrongly_colored_nodes(graph, coloring))
        colors_set = get_colors_set(coloring)
        cost = cost_function(len(wrongly_colored), len(colors_set))
        return cls(graph, coloring, colors_set, cost, wrongly_colored)
