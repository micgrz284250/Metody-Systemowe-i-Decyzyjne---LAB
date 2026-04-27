class Pheromones:
    """
    :param colors: list of all possible colors
    :param pheromones: dict { key: node, value: dict { key: color, value: pheromone level } }
    """
    pheromones = {}
    
    def __init__(self, graph, colors):
        self.colors = colors
        self.pheromones = {node: {color: 1.0 for color in colors} for node in graph.nodes()}

    def vapor_pheromone(self, subtract) -> None:
        for node in self.pheromones:
            for color in self.pheromones[node]:
                self.pheromones[node][color] = max(1.0, self.pheromones[node][color] - subtract)

    def get_pheromone(self, node, color) -> float:
        return self.pheromones[node][color]

    def get_pheromones(self, node) -> dict[int, float]:
        return self.pheromones[node]

    def add_pheromones(self, colored, score) -> None:
        if len(colored) != len(self.pheromones):
            raise ValueError('The number of colored nodes and pheromones do not match')

        for colored_node, color in colored.items():
            self.pheromones[colored_node][color] += score