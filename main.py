from test import show_graph, parse_problem_data_text_to_nx_graph

def main():
    colors = [4, 5, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              0, 1, 2, 3, 0, 0, 2, 1, 3, 0,
              2, 3, 0, 0, 2, 1, 3, 0]
    graph_file = 'instances/anna.col'
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)
    show_graph(problem_graph, colors)

if __name__ == "__main__":
    main()
