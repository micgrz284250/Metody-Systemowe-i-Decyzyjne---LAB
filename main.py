from test import show_graph, parse_problem_data_text_to_nx_graph, evaluate

def main():
    colors_key = [i for i in range(1, 139)]
    colors_values = [i for i in range(1, 139)]
    colors = dict(zip(colors_key, colors_values))
    graph_file = 'instances/anna.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)
    show_graph(problem_graph, colors)
    print(evaluate(problem_graph, colors))

if __name__ == "__main__":
    main()
