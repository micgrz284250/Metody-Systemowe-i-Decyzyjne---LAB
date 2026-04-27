import random


class Ant:
    def __init__(self, id: int, current_node, pheromone_levels):
        self.id = id
        self.current_node = current_node
        self.pheromone_levels = pheromone_levels

    def choose_color(self) -> int:
        color_pheromones_current_node = self.pheromone_levels.get_pheromones(self.current_node)

        total_pheromone = float(sum(color_pheromones_current_node.values()))
        pheromone_draw = random.uniform(0, total_pheromone)

        for color, pheromone in color_pheromones_current_node.items():
            if pheromone_draw < pheromone:
                return color
            pheromone_draw -= pheromone

        raise ValueError('Wring pheromone draw')
