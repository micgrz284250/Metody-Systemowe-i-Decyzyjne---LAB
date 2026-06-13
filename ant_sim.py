import time

from ant_optimization import colony
from test import parse_problem_data_text_to_nx_graph, evaluate

ACO_1_1 = dict(  # optymalne
    num_ants=50, num_iterations=30,
    heuristic_weight=4.0, pheromone_weight=2.0,
    evaporate_value=0.5
)

ACO_1_2 = dict(  # optymalne
    num_ants=30, num_iterations=50,
    heuristic_weight=4.0, pheromone_weight=2.0,
    evaporate_value=0.5
)

ACO_1_3 = dict(  # optymalne
    num_ants=20, num_iterations=75,
    heuristic_weight=4.0, pheromone_weight=2.0,
    evaporate_value=0.5
)

ACO_2 = dict(  # stagnacja feromonowa
    num_ants=10, num_iterations=100,
    heuristic_weight=0.5, pheromone_weight=5.0,
    evaporate_value=0.95
)

ACO_3 = dict(  # zachłanny (feromony ignorowane)
    num_ants=50, num_iterations=30,
    heuristic_weight=4.0, pheromone_weight=0.0,
    evaporate_value=0.1
)

ACO_4 = dict(  # test jednej mrówki, która losowo koloruje
    num_ants=1, num_iterations=1,
    heuristic_weight=0.0, pheromone_weight=0.0,
    evaporate_value=0.1
)

iterations = [ACO_1_1, ACO_1_2, ACO_1_3, ACO_2, ACO_3, ACO_4]

per_iter = 10

graphs = [
    "instances/le450_15b.col",
    "instances/hard_graphs/queen_11x11.col",
    "instances/test_graphs/grid_20x20.col",
    "instances/hard_graphs/hard_3colorable_450.col",
]

# sprawdzanie, czy pliki istnieją
for test_graph in graphs:
    parse_problem_data_text_to_nx_graph(test_graph)

def run_ant_sim():
    for iteration in iterations:
        for graph in graphs:
            problem_graph = parse_problem_data_text_to_nx_graph(graph)
            filename = f"results_{iteration['num_ants']}_{iteration['num_iterations']}_{iteration['heuristic_weight']}_{iteration['pheromone_weight']}_{iteration['evaporate_value']}_{graph.replace(".col", "").replace("instances/", "").replace("test_graphs/", "").replace("hard_graphs/", "")}.txt"

            with open(filename, "w") as f:
                f.write(f"Parameters: {iteration}\n")
                f.write(f"Graph: {graph.replace(".col", "").replace("instances/", "").replace("test_graphs/", "").replace("hard_graphs/", "")}\n")

                for i in range(per_iter):
                    f.write(f"---Run {i+1}---\n")
                    start_time = time.perf_counter()
                    colors, score = colony.optimize(problem_graph,
                                                    num_ants=iteration["num_ants"],
                                                    num_iterations=iteration["num_iterations"],
                                                    heuristic_weight=iteration["heuristic_weight"],
                                                    pheromone_weight=iteration["pheromone_weight"],
                                                    evaporate_value=iteration["evaporate_value"],
                                                    threads=1)
                    end_time = time.perf_counter()
                    f.write(f"Duration: {end_time - start_time} seconds\n")
                    f.write(f"Score: {evaluate(problem_graph, colors)}\n")
                    f.write(f"Result: {colors}\n\n")