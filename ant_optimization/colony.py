from concurrent.futures import ProcessPoolExecutor

from .ant import Ant
from .pheromones import Pheromones


def run_ant(args):
    ant_id, neighbors, pheromones, heuristic_weight, pheromone_weight = args

    # print(f"Starting ant {ant_id}")
    ant = Ant(ant_id, neighbors, pheromones, heuristic_weight, pheromone_weight)
    colors, score = ant.run()
    # print(f"Ant {ant_id} finished with score {score}")

    return ant_id, colors, score


def optimize(graph,
             num_ants=100,
             num_iterations=50,
             heuristic_weight=4.0,
             pheromone_weight=2.0,
             evaporate_value=0.5,
             threads=4):
    ant_id = 1

    neighbors = {node: list(graph.neighbors(node)) for node in graph.nodes}
    pheromones = Pheromones(graph)
    best_colors = None
    best_score = float('inf')

    # print(f"neighbors: {sys.getsizeof(pickle.dumps(neighbors)) / 1024:.1f} KB")
    # print(f"ph_matrix: {sys.getsizeof(pickle.dumps(pheromones)) / 1024:.1f} KB")
    #
    # print(f'Running optimization with {num_iterations} iterations, {num_ants} ants per iteration and {threads} threads')

    with ProcessPoolExecutor(max_workers=threads) as executor:
        for iteration in range(num_iterations):
            print(f'--- Running iteration {iteration} ---')
            solutions = []

            # preparing and data
            ant_args = [
                (ant_id + i, neighbors, pheromones, heuristic_weight, pheromone_weight)
                for i in range(num_ants)
            ]
            ant_id += num_ants

            # process running
            results = executor.map(run_ant, ant_args)

            # result analysis
            for ant_id, colors, score in results:
                solutions.append((colors, score))

                if score < best_score:
                    best_colors = colors
                    best_score = score

            print(f'Best score for ant iteration: {best_score}')

            pheromones.evaporate(evaporate_value)

            for colors, score in solutions:
                pheromones.add_pheromones(colors, score)

            print(f'--- End of iteration {iteration}. Best score so far: {best_score} ---')

    return best_colors, best_score