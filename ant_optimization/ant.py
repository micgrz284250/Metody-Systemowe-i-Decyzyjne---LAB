import random

import numpy as np

from ant_optimization.pheromones import Pheromones


class Ant:
    def __init__(self, ant_id, neighbors, pheromones, heuristic_weight=4.0, pheromone_weight=2.0):
        self.ant_id = ant_id
        # w celu optymalizacji algorytmu sąsiadów przechowujmy w słowniku
        self.neighbors = neighbors
        self.pheromones = pheromones
        self.choosable = set()
        self.blocked = set()
        self.colored = 0
        self.colors = {node: None for node in self.neighbors.keys()}
        self.blocked_count = {node: 0 for node in self.neighbors.keys()}
        self.pheromones_cache = {node: 0.0 for node in self.neighbors.keys()}
        self.heuristic_weight = heuristic_weight
        self.pheromone_weight = pheromone_weight

    def __str__(self):
        return f'Ant {self.ant_id}: colored {self.colored} nodes from all {self.graph.number_of_nodes()} nodes'

    def run(self):
        curr_colors = 1

        # iterujemy, dopóki są jeszcze dostępne niepokolorowane node
        while self.colored < len(self.neighbors):
            self.create_color_subset(curr_colors)
            curr_colors += 1

        return self.colors, len(set(self.colors.values()))

    def reset(self):
        self.choosable = set(node for node in self.colors.keys() if self.colors[node] is None)
        self.blocked = set()
        for node in self.choosable:
            self.pheromones_cache[node] = 0.0

    def get_start_point(self):
        return random.choice(list(self.choosable))

    def remove_neighbors(self, node):
        if node in self.choosable:
            self.choosable.remove(node)

        for neighbor in self.neighbors[node]:
            if neighbor in self.choosable:
                self.choosable.remove(neighbor)

            if neighbor not in self.blocked:
                self.blocked.add(neighbor)

    def update_blocked_count(self, node):
        for neighbor in self.neighbors[node]:
            self.blocked_count[neighbor] += 1

    def update_pheromones_cache(self, node):
        idx = node - 1
        choosable_idx = np.array([n - 1 for n in self.choosable], dtype=np.int32)
        self.pheromones_cache[node] = self.pheromones[idx, choosable_idx].sum()

    def update(self, node):
        self.remove_neighbors(node)
        self.update_blocked_count(node)
        self.update_pheromones_cache(node)

    def create_color_subset(self, color):
        # definiujemy sobie podzbiór node, które będą miały ten sam kolor

        # resetujemy zbiory wybieralnych i zablokowanych
        self.reset()

        # pobieramy startowy node dla zbioru
        start_node = self.get_start_point()
        self.colored += 1
        self.colors[start_node] = color

        # usuwamy sąsiadów startowego node ze zbioru wybieralnych
        self.update(start_node)

        while self.choosable:
            selected_node = self.select_node()
            self.colored += 1
            self.colors[selected_node] = color
            self.update(selected_node)

    def select_node(self):
        nodes = list(self.choosable)
        ph_vals = np.array([self.pheromones_cache[n] for n in nodes])
        bl_vals = np.array([self.blocked_count[n] + 1 for n in nodes], dtype=np.float64)

        weights = (ph_vals ** self.pheromone_weight) * (bl_vals ** self.heuristic_weight)
        total = weights.sum()

        if total == 0:
            return random.choice(nodes)

        weights /= total
        return nodes[np.random.choice(len(nodes), p=weights)]