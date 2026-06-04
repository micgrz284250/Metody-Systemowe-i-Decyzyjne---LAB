import itertools

import numpy as np


class Pheromones:
    def __init__(self, graph):
        self.graph = graph
        self.pheromones = np.ones((graph.number_of_nodes(), graph.number_of_nodes()))


    def evaporate(self, q: float) -> None:
        self.pheromones *= q


    def add_pheromones(self, colors, score) -> None:
        value = 1.0 / score

        color_subsets = {}
        for node, color in colors.items():
            color_subsets.setdefault(color, set()).add(node)

        for color_subset in color_subsets.values():
            if len(color_subset) > 1:
                for node_a, node_b in itertools.combinations(color_subset, 2):
                    self.pheromones[int(node_a)-1, int(node_b)-1] += value
                    self.pheromones[int(node_b)-1, int(node_a)-1] += value

    def get_pheromone(self, node_from: int, node_to: int) -> float:
        return self.pheromones[node_from-1, node_to-1]