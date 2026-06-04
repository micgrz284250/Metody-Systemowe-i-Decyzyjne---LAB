from .ant import Ant
from .pheromones import Pheromones


def optimize(graph, num_ants=100, num_iterations=50, heuristic_weight=4.0, pheromone_weight=2.0, evaporate_value=0.5, threads=1):
    pheromones = Pheromones(graph)

    best_colors = None
    best_score = float('inf')

    ant_id = 1
    for iteration in range(num_iterations):
        print(f'--- Running iteration {iteration} ---')

        solutions = []
        for ant in range(num_ants):
            print(f'Running ant {ant_id}...')

            ant = Ant(ant_id, graph, pheromones, heuristic_weight, pheromone_weight)
            colors, score = ant.run()
            solutions.append((colors, score))

            if score < best_score:
                best_colors = colors
                best_score = score

            print(f'Ant {ant_id} found solution with score {score}. Best score so far: {best_score}')

            ant_id += 1
        pheromones.evaporate(evaporate_value)

        for colors, score in solutions:
            pheromones.add_pheromones(colors, score)

        print(f'--- End of iteration {iteration}. Best score so far: {best_score} ---')

    return best_colors, best_score