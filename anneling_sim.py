import resource
import tracemalloc

from simulated_annealing.simulation import get_iteration_generator
from test import parse_problem_data_text_to_nx_graph, evaluate


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

    for it in get_iteration_generator(problem_graph, is_right):
        print(it.cost)
        print()

    tracemalloc.start()

    print(
        set(
            it.cost
            for it in get_iteration_generator(problem_graph, iterations(10000))
            if not it.wrongly_colored_nodes
        )
    )

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    print(f"tracemalloc peak: {peak / 1024 / 1024:.1f} MB")
    print(f"RSS peak:         {rss / 1024:.1f} MB")

    print(f'Found solution: {it.result}')
    print(f'Evaluated {evaluate(problem_graph, it.result)}')

    # for it in get_iteration_generator(problem_graph, lambda x: x.temperature is not None and x.temperature == 0):
    #     print(it.temperature)
    #     print(evaluate(problem_graph, it.result))


if __name__ == "__main__":
    main()
