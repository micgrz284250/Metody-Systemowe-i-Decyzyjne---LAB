"""Module providing Graph class"""
from dataclasses import dataclass



@dataclass(frozen=True)
class Graph:
    """Class representing graph object by neighbour list for every verticle"""
    no_nodes: int
    no_edges: int
    neighbour_lists: list[list[int]]
    colors_list: list[int]
