class Ant:
    """
        :param ant_id
        :param graph - graph on which ant will run
        :param current_node - current node on which ant is located
        :param pheromone_levels - dictionary of pheromone levels for each node
        :param pheromone_function - function to calculate float value of chance of choosing a node based on its pheromone level
    """
    def __init__(self, ant_id, graph, current_node, pheromone_levels, pheromone_function):
        self.ant_id = ant_id
        self.graph = graph
        self.current_node = current_node
        self.pheromone_levels = pheromone_levels
        self.pheromone_function = pheromone_function


    # def choose_color(self) -> int:
    #     color_pheromones_current_node = self.pheromone_levels.get_pheromones(self.current_node)
    #
    #     total_pheromone = float(sum(color_pheromones_current_node.values()))
    #     pheromone_draw = random.uniform(0, total_pheromone)
    #
    #     for color, pheromone in color_pheromones_current_node.items():
    #         if pheromone_draw < pheromone:
    #             return color
    #         pheromone_draw -= pheromone
    #
    #     raise ValueError('Wrong pheromone draw')

    def run_ant(self):
        return