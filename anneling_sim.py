import time
from math import inf

from simulated_annealing.simulation import get_iteration_generator
from test import parse_problem_data_text_to_nx_graph, evaluate


def main():
    graph_file = "instances/hard_graphs/hard_3colorable_450.col"
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)

    def iterations(no_iteration):
        iteration = 0

        def count_next(_):
            nonlocal iteration
            iteration += 1
            return iteration == no_iteration

        return count_next

    def is_right(it):
        return not bool(it.wrongly_colored_nodes)

    def optimize_result(result):
        col_range = len(set(result.values()))

    iteration_list = [1000, 10000, 100000]
    for iteration in iteration_list:
        print(f'Iteration {iteration}')
        for i in range(10):
            print(f'Run {i + 1}')
            best_res = {}
            best_score = inf
            start = time.perf_counter()

            for it in get_iteration_generator(problem_graph, iterations(iteration)):
                score = len(it.colors_used) if len(it.wrongly_colored_nodes) == 0 else inf
                if score < best_score or best_res == {}:
                    best_score = len(it.colors_used)
                    best_res = it.result

            end = time.perf_counter()

            print(f'Elapsed time: {end - start} seconds')
            print(f'Found solution: {best_res}')
            print(f'Score: {best_score}')
            print(f'Evaluated {evaluate(problem_graph, best_res)}')




if __name__ == "__main__":
    main()
