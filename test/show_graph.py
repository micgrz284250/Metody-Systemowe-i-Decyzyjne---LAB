"""This module constains functions used to visualise nx.Graph instance"""
import networkx as nx
import matplotlib.pyplot as plt

def show_graph(graph: nx.Graph) -> None:
    """Shows graph visualistion from nx.Graph object"""
    pos = nx.kamada_kawai_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    plt.show()
