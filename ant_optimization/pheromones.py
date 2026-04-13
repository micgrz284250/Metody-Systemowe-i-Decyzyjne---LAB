from collections.abc import Hashable


class Pheromones:
    pheromone_graph = {}

    def __init__(self, graph, colors):
        self.graph = graph
        self.colors = colors
        self.pheromone_graph = {node: {color: 0.0 for color in colors} for node in graph.nodes()}

    def vapor_pheromone(self, subtract) -> None:
        for node in self.pheromone_graph:
            for color in self.pheromone_graph[node]:
                self.pheromone_graph[node][color] = max(0, self.pheromone_graph[node][color] - subtract)

    def get_pheromone(self, node, color) -> float:
        return self.pheromone_graph[node][color]

    def get_pheromones(self, node) -> dict[Hashable, float]:
        return self.pheromone_graph[node]

    def add_pheromones(self, colored, score) -> None:
        if len(colored) != len(self.pheromone_graph):
            raise ValueError('The number of colored nodes and pheromones do not match')

        for colored_node, color in colored.items():
            self.pheromone_graph[colored_node][color] += score