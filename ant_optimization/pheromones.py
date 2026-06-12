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
            color_subsets.setdefault(color, []).append(int(node) - 1)

        for subset in color_subsets.values():
            if len(subset) > 1:
                idx = np.array(subset, dtype=int)
                self.pheromones[np.ix_(idx, idx)] += value

    def get_pheromone(self, node_from: int, node_to: int) -> float:
        return self.pheromones[int(node_from)-1, int(node_to)-1]