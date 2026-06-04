from ant_optimization import colony
from test import parse_problem_data_text_to_nx_graph, show_graph


def main():
    graph_file = 'instances/anna.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)
    colors = colony.optimize(problem_graph, num_ants=10, num_iterations=5)
    show_graph(problem_graph, colors)

if __name__ == "__main__":
    main()
