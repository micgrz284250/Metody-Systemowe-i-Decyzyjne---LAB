from ant_optimization import colony
from test import parse_problem_data_text_to_nx_graph, show_graph


def main():
    graph_file = 'instances/le450_15b.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)
    colors, score = colony.optimize(problem_graph, num_ants=10, num_iterations=10, heuristic_weight=4.0)
    print(f'Found solution: {colors}')
    print(f'Score: {score}')
    show_graph(problem_graph, colors)

if __name__ == "__main__":
    main()
