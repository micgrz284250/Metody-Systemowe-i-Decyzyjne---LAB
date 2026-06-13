import networkx as nx

from ant_optimization import colony
from test import parse_problem_data_text_to_nx_graph, show_graph, evaluate
import tracemalloc
import resource
import time


def main():
    graph_file = 'hard_graphs/hard_3colorable_450.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)

    # print(len(problem_graph.nodes))

    tracemalloc.start()

    iteration_list = [(1, 1), (50, 20), (100, 10), (50, 20), (10, 100)]

    # G = nx.mycielski_graph(8)
    # col = nx.coloring.greedy_color(G, strategy='largest_first')
    # print(max(col.values()) + 1)

    for iteration in iteration_list:
        num_ants, iterations = iteration
        for i in range(10):
            start = time.perf_counter()
            colors, score = colony.optimize(problem_graph, num_ants=num_ants, num_iterations=iterations, heuristic_weight=4.0, pheromone_weight=2.0, evaporate_value=0.5, threads=1)
            end = time.perf_counter()

            print(f'Elapsed time: {end - start} seconds')
            print(f'Found solution: {colors}')
            print(f'Score: {score}')
            print(f'Evaluated {evaluate(problem_graph, colors)}')

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # w KB na Linuxie

    # print(f"tracemalloc peak: {peak / 1024 / 1024:.1f} MB")
    # print(f"RSS peak:         {rss / 1024:.1f} MB")

    # show_graph(problem_graph, colors)

def show():
    graph_file = 'hard_graphs/hard_3colorable_450.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)
    colors = {node: 1 for node in problem_graph.nodes()}
    show_graph(problem_graph, colors)

if __name__ == "__main__":
    show()
    main()
