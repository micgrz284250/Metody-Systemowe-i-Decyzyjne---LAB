"""Default starting point to see graph visualistaion"""

if __name__ == '__main__':
    from test.parser import parse_problem_data_text_to_nx_graph
    from test.show_graph import show_graph
    GRAPH_FILE = 'instances/anna.col'
    problem_graph = parse_problem_data_text_to_nx_graph(GRAPH_FILE)
    show_graph(problem_graph)
