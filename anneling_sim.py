import time
from math import inf, sqrt

from simulated_annealing.simulation import get_iteration_generator
from test import parse_problem_data_text_to_nx_graph, evaluate

SA_1 = dict(  # optymalne
    cooling_rate=0.9995,
)

SA_2 = dict(  # za wolne chłodzenie (eksploracja bez zbieżności)
    cooling_rate=0.9999,
)

iterations_data = [
    SA_1,
    # SA_2
]

iterations_count = [
    1000,
    # 1500
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

def run_sa_sim(graphs: list[str], per_iter: int):
    for iteration in iterations_data:
        for count in iterations_count:
            for graph in graphs:
                #szykowanie grafu
                problem_graph = parse_problem_data_text_to_nx_graph(graph)
                adj_dict = {node: list(problem_graph.neighbors(node)) for node in problem_graph.nodes}

                #szykowanie parametrów
                fixed_count = count * problem_graph.number_of_nodes()
                num_starting_colors = int(max(10, sqrt(problem_graph.number_of_nodes())))

                print(num_starting_colors)

                for sub_count in [count, fixed_count]:
                    #szykowanie cooling
                    fixed_cooling = 0.00001**(1/sub_count)

                    for num_of_colors in [num_starting_colors, problem_graph.number_of_nodes()]:
                        for cooling in [iteration["cooling_rate"], fixed_cooling]:
                            print(sub_count, num_of_colors, cooling)

                            filename = f"SA_results_{cooling}_{sub_count}_{num_of_colors}_{graph.replace(".col", "").replace("pograzajace_ACO/", "").replace("instances/", "").replace("test_graphs/", "").replace("hard_graphs/", "")}.txt"

                            with open(filename, "w") as f:
                                f.write(f"cooling {cooling} count {sub_count} num of colors {num_of_colors}\n")
                                f.write(f"Graph: {graph.replace(".col", "").replace("instances/", "").replace("pograzajace_ACO/", "").replace("test_graphs/", "").replace("hard_graphs/", "")}\n")

                                for i in range(per_iter):
                                    f.write(f"---Run {i+1}---\n")

                                    best_res = {}
                                    best_score = inf

                                    start_time = time.perf_counter()

                                    i = 0
                                    for it in get_iteration_generator(adj=adj_dict,
                                                                      ending_condition=iterations(sub_count),
                                                                      cooling_rate=cooling,
                                                                      starting_no_colors=num_of_colors):
                                        score = len(it.colors_used) if len(it.wrongly_colored_nodes) == 0 else inf
                                        i += 1
                                        if i % 1000 == 0:
                                            print(i)
                                        if score < best_score or best_res == {}:
                                            best_score = len(it.colors_used)
                                            best_res = it.result

                                    end_time = time.perf_counter()

                                    f.write(f"Duration: {end_time - start_time} seconds\n")
                                    f.write(f"Score: {evaluate(problem_graph, best_res)}\n")
                                    f.write(f"Result: {minimize_colors_dict(best_res)}\n\n")

'''
zmienne parametry
cooling rate: 0.9995 albo wyliczane dynamicznie
iter count: 1000 lub 1000 * liczba wierzchołków (poprawka względem mrówkowego)
początkowa liczba kolorów: sqrt(node) lub node
'''