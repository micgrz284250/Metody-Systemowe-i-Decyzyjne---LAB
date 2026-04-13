# https://home.agh.edu.pl/~slukasik/pub/008_Lukasik_Kokosinski_Swieton_LNCS_PPAM2007.pdf
from typing import Generator
from dataclasses import dataclass
import copy
import math
import random

import networkx as nx


@dataclass(frozen=True)
class Iteration:
    graph: nx.Graph
    result: dict[int, int]
    colors_used: frozenset[int]
    cost: int
    wrongly_colored_nodes: list[int]

    @classmethod
    def get_nxt_iteration(
        cls, graph: nx.Graph, coloring: dict[int, int]
    ):
        wrongly_colored = list(get_wrongly_colored_nodes(graph, coloring))
        colors_set = get_colors_set(coloring)
        cost = cost_function(len(wrongly_colored), len(colors_set))
        return cls(graph, coloring, colors_set, cost, wrongly_colored)


def get_wrongly_colored_nodes(graph: nx.Graph, colors: dict[int, int]) -> Generator:
    """Return nodes with neighbours sharing same color"""
    if graph.number_of_nodes() != len(colors):
        raise ValueError("Graph and colors mismatch")

    return (
        node
        for node in graph.nodes
        for neighbour in graph.neighbors(node)
        if colors[int(node)] == colors[int(neighbour)]
    )


def get_colors_set(colors: dict[int, int]) -> int:
    return {color for _, color in colors.items()}


def cost_function(
    no_wrongly_colored: int, no_colors: int, wrong_node_cost_mult: int = 2
) -> int:
    """Get the cost of current iteration"""
    return no_wrongly_colored * wrong_node_cost_mult + no_colors


def temperature_function(
    prev_iteration: Iteration, cooling_rate: float = 0.95
) -> float:
    return prev_iteration * cooling_rate

def get_prob_from_temp(temperature: float, cost_diff: float):
    return math.exp(- cost_diff / temperature)


def get_with_new_color(dict_: dict[int, int], node: int, color: int):
    new_dict = dict_.copy()
    new_dict[node] = color
    return new_dict


def get_starting_iteration(graph: nx.Graph):
    pass

def get_nxt_coloring(iteration: Iteration):
    if iteration.wrongly_colored_nodes:
        updated_node = random.choice(list(iteration.wrongly_colored_nodes))
        # Jest możliwość, że liczba kolorów nie wystarcza, więc zwiększamy ją o 1
        updated_color = random.choice(
            list(iteration.colors_used) + [max(iteration.colors_used)]
        )
        return get_with_new_color(
            iteration.result, int(updated_node), int(updated_color)
        )
    updated_node = random.choice(list(graph))
    updated_color = random.choice(list(iteration.colors_used))
    return get_with_new_color(
        iteration.result, int(updated_node), int(updated_color)
    )


def get_iteration_function(graph: nx.Graph, ending_condition = lambda _ : False):
    """One iteration of simulated anneling"""

    iteration = get_starting_iteration(graph)
    temperature = 99.9
    while not ending_condition:
        yield iteration
        new_coloring = get_nxt_coloring(iteration)
        new_iteration = Iteration.get_nxt_iteration(graph, new_coloring)
        cost_diff = new_iteration.cost - iteration.cost
        if cost_diff < 0:
            iteration = new_iteration
        else:
            acceptance_prob = get_prob_from_temp(temperature, cost_diff)
            if random.random() < acceptance_prob:
                iteration = new_iteration
            else:
                iteration = copy.deepcopy(iteration)
