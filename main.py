import time

from ant_optimization import colony
from test import parse_problem_data_text_to_nx_graph, show_graph, evaluate


def main():
    graph_file = 'instances/le450_15b.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)

    iteration_list = [(1, 1), (2, 50), (100, 10), (50, 20), (10, 100)]

    for iteration in iteration_list:
        num_ants, iterations = iteration
        for i in range(10):
            start = time.perf_counter()
            colors, score = colony.optimize(problem_graph, num_ants=num_ants, num_iterations=iterations, heuristic_weight=4.0, pheromone_weight=2.0, evaporate_value=0.5, threads=16)
            end = time.perf_counter()

            print(f'Elapsed time: {end - start} seconds')
            print(f'Found solution: {colors}')
            print(f'Score: {score}')
            print(f'Evaluated {evaluate(problem_graph, colors)}')

    # show_graph(problem_graph, colors)

def show():
    graph_file = 'instances/hard_graphs/petersen_40_6.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)
    colors = {node: 1 for node in problem_graph.nodes()}
    show_graph(problem_graph, colors)

if __name__ == "__main__":
    # show()
    main()
