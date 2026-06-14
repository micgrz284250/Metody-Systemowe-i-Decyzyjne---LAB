from test import parse_problem_data_text_to_nx_graph, show_graph

def show(graphs: list[str]):
    for graph in graphs:
        problem_graph = parse_problem_data_text_to_nx_graph(graph)
        show_graph(problem_graph)