import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import logging
logger = logging.getLogger(__name__)


def show_graph(graph: nx.Graph, colors: dict[int, int] = None) -> None:
    """
    Graph visualization
    This function allows to visualize a nx.Graph instance
    :param graph: Graph to visualize
    :param colors: Optional, list of colors for each node
    """

    # Check if colors are provided and match the number of nodes
    if colors is not None and graph.number_of_nodes() != len(colors):
        raise ValueError(f'Graph and colors mismatch, nodes: {graph.number_of_nodes()} != {len(colors)}')

    plt.figure(figsize=(16, 12))

    # spring_layout - lepszy dla gęstych grafów
    pos = nx.spring_layout(graph, k=0.5, iterations=50, seed=42)

    # Rysowanie z mniejszymi węzłami i tekstem
    if colors is not None:
        colors_hex = generate_colors(colors)

        logger.debug(colors)
        logger.debug(colors_hex)

        colors_list = [colors_hex[int(node)] for node in graph.nodes()]
        nx.draw_networkx_nodes(graph, pos, node_color=colors_list, node_size=300, edgecolors='black', linewidths=0.5)
    else:
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue', node_size=300, edgecolors='black', linewidths=0.5)

    nx.draw_networkx_edges(graph, pos, width=0.5, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=7)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def generate_colors(colors: dict[int, int]) -> dict[int, str]:
    max_value = max(colors.values())
    min_value = min(colors.values())
    n = max_value - min_value + 1
    cmap = plt.get_cmap('hsv', n)
    colors_hex = [mcolors.to_hex(cmap(i)) for i in range(n)]
    print(colors)
    print(len(colors_hex))
    return dict(zip(colors.keys(), [colors_hex[int(node - min_value)] for node in colors.values()]))