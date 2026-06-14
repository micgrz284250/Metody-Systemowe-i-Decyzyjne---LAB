from anneling_sim import run_sa_sim
from ant_sim import run_ant_sim
from show import show

graphs = [
    "instances/hard_graphs/queen_11x11.col",
    "instances/le450_15b.col",
    "instances/test_graphs/grid_20x20.col",
    "instances/test_graphs/cliques_8x12_bridges.col",
]

def main():
    show(graphs)
    run_sa_sim(graphs, 10)
    run_ant_sim(graphs, 10)

if __name__ == "__main__":
    main()