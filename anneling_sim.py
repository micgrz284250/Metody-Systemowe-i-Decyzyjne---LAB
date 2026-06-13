import time
from math import inf

from simulated_annealing.simulation import get_iteration_generator
from test import parse_problem_data_text_to_nx_graph, evaluate

SA_1 = dict(  # optymalne
    cooling_rate=0.9995,
)

SA_2 = dict(  # za szybkie chłodzenie (stagnacja)
    cooling_rate=0.99,
)

SA_3 = dict(  # za wolne chłodzenie (eksploracja bez zbieżności)
    cooling_rate=0.9999,
)

iterations_data = [SA_1, SA_2, SA_3]
iterations_count = [1, 100, 1000, 1500]

per_iter = 10

graphs = [
    "instances/le450_15b.col",
    "instances/hard_graphs/queen_11x11.col",
    "instances/test_graphs/grid_20x20.col",
    "instances/hard_graphs/hard_3colorable_450.col",
]


def iterations(no_iteration):
    iteration_ = 0

    def count_next(_):
        nonlocal iteration_
        iteration_ += 1
        return iteration_ > no_iteration

    return count_next

def minimize_colors_dict(colors):
    rank = {v: i + 1 for i, v in enumerate(sorted(set(colors.values())))}
    result = {k: rank[v] for k, v in colors.items()}
    return result

def run_sa_sim():
    for iteration in iterations_data:
        for count in iterations_count:
            for graph in graphs:
                problem_graph = parse_problem_data_text_to_nx_graph(graph)
                fixed_count = count * problem_graph.number_of_nodes()
                for sub_count in [count, fixed_count]:
                    print(sub_count)

                    filename = f"SA_results_{iteration['cooling_rate']}_{sub_count}_{graph.replace(".col", "").replace("instances/", "").replace("test_graphs/", "").replace("hard_graphs/", "")}.txt"

                    with open(filename, "w") as f:
                        f.write(f"Parameters: {iteration} count={sub_count}\n")
                        f.write(f"Graph: {graph.replace(".col", "").replace("instances/", "").replace("test_graphs/", "").replace("hard_graphs/", "")}\n")

                        for i in range(per_iter):
                            f.write(f"---Run {i+1}---\n")

                            best_res = {}
                            best_score = inf

                            start_time = time.perf_counter()

                            for it in get_iteration_generator(graph=problem_graph,
                                                              ending_condition=iterations(sub_count),
                                                              cooling_rate=iteration["cooling_rate"]):
                                score = len(it.colors_used) if len(it.wrongly_colored_nodes) == 0 else inf
                                if score < best_score or best_res == {}:
                                    best_score = len(it.colors_used)
                                    best_res = it.result

                            end_time = time.perf_counter()

                            f.write(f"Duration: {end_time - start_time} seconds\n")
                            f.write(f"Score: {evaluate(problem_graph, best_res)}\n")
                            f.write(f"Result: {minimize_colors_dict(best_res)}\n\n")