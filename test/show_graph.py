import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx


def show_graph(graph: nx.Graph, colors: list[int] = None) -> None:
    """
    Graph visualization
    This function allows to visualize a nx.Graph instance
    :param graph: Graph to visualize
    :param colors: Optional, list of colors for each node
    """

    # Check if colors are provided and match the number of nodes
    if colors is not None and graph.number_of_nodes() != len(colors):
        raise ValueError(f'Graph and colors mismatch, nodes: {graph.number_of_nodes()} != {len(colors)}')

    # if colors is not None:
    #     colors_hex = generate_colors(colors)
    #     for (node, color) in zip(graph.nodes(), colors_hex):
    #         node['color'] = color

    plt.figure(figsize=(16, 12))

    # spring_layout - lepszy dla gęstych grafów
    pos = nx.spring_layout(graph, k=0.5, iterations=50, seed=42)

    # Rysowanie z mniejszymi węzłami i tekstem
    if colors is not None:
        print(graph.nodes())
        for node, color in zip(graph.nodes(), colors):
            print(f'Node: {node}, color: {color}')
        nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=300, edgecolors='black', linewidths=0.5)
    else:
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue', node_size=300, edgecolors='black', linewidths=0.5)
    nx.draw_networkx_edges(graph, pos, width=0.5, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=7)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def generate_colors(colors: list[int]) -> list[str]:
    max_value = max(colors)
    min_value = min(colors)
    n = max_value - min_value + 1
    cmap = plt.get_cmap('tab20', n)
    color_list = [mcolors.to_hex(cmap(i)) for i in range(n)]
    print(type(color_list[0]))
    return color_list