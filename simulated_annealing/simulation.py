"""
Simulation algorithm implementation. Inspired by:
https://home.agh.edu.pl/~slukasik/pub/008_Lukasik_Kokosinski_Swieton_LNCS_PPAM2007.pdf
"""

from typing import Generator
from simulated_annealing.parameters import *
import math
import random
import statistics
import networkx as nx

from simulated_annealing.iteration import Iteration


def get_wrongly_colored_nodes(graph: nx.Graph, colors: dict[str, int]) -> Generator:
    """
    Returns nodes with neighbours sharing same color. Each node can apear multiple times.
    Used for cost counting purposes
    """
    if graph.number_of_nodes() != len(colors):
        raise ValueError("Graph and colors mismatch")

    return (
        node
        for node in graph.nodes
        for neighbour in graph.neighbors(node)
        if colors[node] == colors[neighbour]
    )


def get_colors_set(colors: dict[str, int]) -> frozenset[int]:
    """Returns set of used colors"""
    return frozenset(color for _, color in colors.items())


def cost_function(
    no_wrongly_colored: int,
    no_colors: int,
    wrong_node_cost_mult: int = WRONG_NODE_COST_MULT,
) -> int:
    """Get the cost of current iteration"""
    return no_wrongly_colored * wrong_node_cost_mult + no_colors


def temperature_function(temp: float, cooling_rate: float = COOLING_RATE) -> float:
    """Returns updated temperature"""
    return temp * cooling_rate


def get_prob_from_temp(temperature: float, cost_diff: float):
    """Returns probability of acceptance"""
    return math.exp(-cost_diff / temperature)


def get_starting_temp(positive_cost_diffs: list[float], desired_acceptance_prob: float):
    """Returns start temperature for simulation"""
    avg_diff = statistics.mean(positive_cost_diffs)
    return -avg_diff / math.log(desired_acceptance_prob)


def get_with_new_color(dict_: dict[str, int], node: str, color: int):
    """Returns new dict with edited colors"""
    new_dict = dict_.copy()
    new_dict[node] = color
    return new_dict


def get_random_coloring(graph: nx.Graph, no_colors: int):
    """Returns random coloring for graph"""
    return {verticle: random.randint(1, no_colors) for verticle in graph}


def get_starting_data(
    graph: nx.Graph,
    starting_no_colors: int,
    no_pilot_iteration: int,
    desired_acceptance_prob,
):
    """Returns tuple (starting_iteration, starting temperature)"""
    starting_colors = get_random_coloring(graph, starting_no_colors)
    prev_iter = None
    curr_iter = Iteration.get_iteration(graph, starting_colors, None)
    positive_cost_diffs = []
    # Bierzemy pod uwagę średnią dodatnią zmianę kosztu
    iter_idx = 0
    while iter_idx < no_pilot_iteration:
        prev_iter = curr_iter
        curr_iter = Iteration.get_iteration(graph, get_nxt_coloring(prev_iter), None)
        cost_diff = curr_iter.cost - prev_iter.cost
        if cost_diff > 0:
            positive_cost_diffs.append(curr_iter.cost)
            iter_idx += 1
    return (curr_iter, get_starting_temp(positive_cost_diffs, desired_acceptance_prob))


def get_nxt_coloring(iteration: Iteration):
    """Returns updated coloring for next iteration"""
    if iteration.wrongly_colored_nodes:
        updated_node = random.choice(list(iteration.wrongly_colored_nodes))
        # Jest możliwość, że liczba kolorów nie wystarcza, więc zwiększamy ją o 1
        updated_color = random.choice(
            list(iteration.colors_used) + [max(iteration.colors_used) + 1]
        )
        return get_with_new_color(iteration.result, updated_node, int(updated_color))
    updated_node = random.choice(list(iteration.graph))
    updated_color = random.choice(list(iteration.colors_used))
    return get_with_new_color(iteration.result, updated_node, int(updated_color))


def get_iteration_generator(
    graph: nx.Graph,
    ending_condition=lambda _: False,
    starting_no_colors: int = STARTING_NO_COLORS,
    no_pilot_iterations: int = NO_PILOT_ITERATIONS,
    desired_acceptance_prob: float = DESIRED_ACCEPTANCE_PROB,
):
    """Iterator of simulated anneling"""
    iteration, temperature = get_starting_data(
        graph, starting_no_colors, no_pilot_iterations, desired_acceptance_prob
    )
    while not ending_condition(iteration):
        yield iteration
        new_coloring = get_nxt_coloring(iteration)
        new_iteration = Iteration.get_iteration(graph, new_coloring, temperature)
        cost_diff = new_iteration.cost - iteration.cost
        if cost_diff < 0:
            iteration = new_iteration
        else:
            acceptance_prob = get_prob_from_temp(temperature, cost_diff)
            if random.random() < acceptance_prob:
                iteration = new_iteration
        temperature = temperature_function(temperature)
