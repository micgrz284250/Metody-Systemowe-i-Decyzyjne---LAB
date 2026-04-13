class Ant:
    def __init__(self, id, current_node, pheromone_levels):
        self.id = id
        self.current_node = current_node
        self.pheromone_levels = pheromone_levels

    def choose_color(self):
        color_pheromones_current_node = self.pheromone_levels.get_pheromones(self.current_node)
