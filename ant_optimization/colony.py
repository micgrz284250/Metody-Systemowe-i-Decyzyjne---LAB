from .ant import Ant
from .pheromones import Pheromones


def optimize(graph, num_ants=100, num_iterations=50, heuristic_weight=4.0, pheromone_weight=2.0, evaporate_value=0.5, threads=1):
    pheromones = Pheromones(graph)

    best_colors = None
    best_score = float('inf')
    solutions = []

    ant_id = 1
    for iteration in range(num_iterations):
        for ant in range(num_ants):
            ant = Ant(ant_id, graph, pheromones, heuristic_weight, pheromone_weight)
            colors, score = ant.run()
            solutions.append((colors, score))

            if score < best_score:
                best_colors = colors
                best_score = score

            ant_id += 1
        pheromones.evaporate(evaporate_value)

        for colors, score in solutions:
            pheromones.add_pheromones(colors, score)

    return best_colors