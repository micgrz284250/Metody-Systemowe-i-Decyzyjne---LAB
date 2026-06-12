from ant_optimization import colony
from test import parse_problem_data_text_to_nx_graph, show_graph, evaluate



def main():
    graph_file = 'instances/school1_nsh.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)

    print(len(problem_graph.nodes))

    colors, score = colony.optimize(problem_graph, num_ants=100, num_iterations=100, heuristic_weight=2.0, pheromone_weight=3.0, evaporate_value=0.5, threads=16)

    print(f'Found solution: {colors}')
    print(f'Score: {score}')
    print(f'Evaluated {evaluate(problem_graph, colors)}')

    # show_graph(problem_graph, colors)

if __name__ == "__main__":
    main()
