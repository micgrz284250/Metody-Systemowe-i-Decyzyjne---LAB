import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import logging
import random
logger = logging.getLogger(__name__)


def show_graph(graph: nx.Graph, colors: dict[int, int] = None) -> None:
    """
    Graph visualization
    This function allows to visualize a nx.Graph instance
    :param graph: Graph to visualize
    :param colors: Optional, list of colors for each node
    """
    # sprawdzanie zgodności
    if colors is not None and graph.number_of_nodes() != len(colors):
        raise ValueError(f'Graph and colors mismatch, nodes: {graph.number_of_nodes()} != {len(colors)}')

    # --- POPRAWKA: Filtrujemy węzły bez krawędzi (samotne wyspy) ---
    nodes_with_edges = [node for node in graph.nodes() if graph.degree(node) > 0]
    subgraph = graph.subgraph(nodes_with_edges)

    plt.figure(figsize=(16, 12))

    # Zmiana layoutu na lepszy dla gęstych, złączonych struktur
    pos = nx.kamada_kawai_layout(subgraph)

    if colors is not None:
        colors_hex = generate_colors(colors)

        # Pobieramy kolory TYLKO dla węzłów, które rysujemy
        colors_list = [colors_hex[int(node)] for node in subgraph.nodes()]

        nx.draw_networkx_nodes(subgraph, pos, node_color=colors_list, node_size=150, edgecolors='black', linewidths=0.5)
    else:
        nx.draw_networkx_nodes(subgraph, pos, node_color='lightblue', node_size=150, edgecolors='black', linewidths=0.5)

    nx.draw_networkx_edges(subgraph, pos, width=0.3, alpha=0.4)

    # Wyłączenie etykiet (numerków) mocno poprawia czytelność przy 500+ węzłach
    # nx.draw_networkx_labels(subgraph, pos, font_size = 7)

    plt.axis('off')
    plt.tight_layout()
    plt.show()


def generate_colors(colors: dict[int, int]) -> dict[int, str]:
    max_value = max(colors.values())
    min_value = min(colors.values())
    n = max_value - min_value + 1

    if n <= 20:
        c_map = plt.get_cmap('tab20')
        colors_hex = [mcolors.to_hex(c_map(i)) for i in range(n)]
    else:
        c_map = plt.get_cmap('nipy_spectral')

        # 1. Generujemy równomierne ułamki od 0.0 do 1.0
        fractions = [i / n for i in range(n)]

        # 2. KLUCZOWA ZMIANA: Mieszamy ułamki!
        # Używamy obiektu random z ustawionym ziarnem (seed), aby tasowanie
        # było identyczne przy każdym odpaleniu programu (kolory nie będą skakać)
        random.Random(42).shuffle(fractions)

        # 3. Przypisujemy przetasowane ułamki do palety
        colors_hex = [mcolors.to_hex(c_map(f)) for f in fractions]

    return dict(zip(colors.keys(), [colors_hex[color_id - min_value] for color_id in colors.values()]))
