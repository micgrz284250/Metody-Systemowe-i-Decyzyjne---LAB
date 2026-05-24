from test import parse_problem_data_text_to_nx_graph
from simulated_annealing.simulation import get_iteration_function


def main():
    graph_file = "instances/anna.col"
    problem_graph = parse_problem_data_text_to_nx_graph(graph_file)

    def iterations(no_iteration):
        iteration = 0

        def count_next(_):
            nonlocal iteration
            iteration += 1
            return iteration == no_iteration

        return count_next

    def is_right(it):
        return not bool(it.wrongly_colored_nodes)

    for it in get_iteration_function(problem_graph, is_right):
        print(it.cost)
        print()

    print(
        set(
            it.cost
            for it in get_iteration_function(problem_graph, iterations(10000000))
            if not it.wrongly_colored_nodes
        )
    )


if __name__ == "__main__":
    main()
