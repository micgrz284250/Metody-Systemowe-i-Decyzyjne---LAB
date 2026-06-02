import numpy as np


class Pheromones:
    def __init__(self, graph):
        self.graph = graph
        self.pheromones = np.ones((graph.number_of_nodes(), graph.number_of_nodes()))

    def vapor_pheromone(self, q: float) -> None:
        self.pheromones - q

    def get_pheromone(self, node_from: int, node_to: int) -> float:
        return self.pheromones[node_from, node_to]