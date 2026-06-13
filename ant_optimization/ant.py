import random
import numpy as np


class Ant:
    def __init__(self, ant_id, adj, pheromones, heuristic_weight=4.0, pheromone_weight=2.0):
        self.ant_id = ant_id
        # w celu optymalizacji algorytmu sąsiadów przechowujmy w słowniku
        self.adj = adj
        # nie potrzebujemy referencji do całego feromonu, wystarczy macierz
        self.pheromones = pheromones.values

        self.choosable = set()
        self.blocked = set()
        self.colors = {node: None for node in self.adj.keys()}

        self.blocked_cache = {node: 0 for node in self.adj.keys()}
        self.pheromones_cache = {node: 0.0 for node in self.adj.keys()}

        self.heuristic_weight = heuristic_weight
        self.pheromone_weight = pheromone_weight

    def __str__(self):
        return f'Ant {self.ant_id}: colored {len(list(node for node in self.colors.keys() if self.colors[node] is not None))} nodes from all {len(self.adj)} nodes'

    def run(self):
        curr_colors = 1
        self.reset()

        # iterujemy, dopóki są jeszcze dostępne niepokolorowane node
        while self.choosable:
            self.create_color_subset(curr_colors)
            curr_colors += 1
            self.reset()

        return self.colors, len(set(self.colors.values()))

    def reset(self):
        self.choosable = set(node for node in self.colors.keys() if self.colors[node] is None)
        self.blocked = set()
        for node in self.choosable:
            self.pheromones_cache[node] = 0.0

    def get_start_point(self):
        return random.choice(list(self.choosable))

    def update_subsets(self, node):
        if node in self.choosable:
            self.choosable.remove(node)

        for neighbor in self.adj[node]:
            if neighbor in self.choosable:
                self.choosable.remove(neighbor)

            if neighbor not in self.blocked:
                self.blocked.add(neighbor)

    def update_blocked_count(self, node):
        if node in self.blocked:
            for neighbor in self.adj[node]:
                self.adj[neighbor] += 1

    def update_pheromones_cache(self, node):
        for sec_node in self.choosable:
            self.pheromones_cache[sec_node] += self.pheromones[int(node) - 1, int(sec_node) - 1]

    def update(self, node):
        self.update_subsets(node)
        self.update_blocked_count(node)
        self.update_pheromones_cache(node)

    def create_color_subset(self, color):
        # definiujemy podzbiór node, które będą miały ten sam kolor

        # resetujemy zbiory wybieralnych i zablokowanych
        self.reset()

        # pobieramy startowy node dla zbioru
        start_node = self.get_start_point()
        self.colors[start_node] = color

        # aktualizujemy stan mrówki
        self.update(start_node)

        while self.choosable:
            selected_node = self.select_node()
            self.colors[selected_node] = color
            self.update(selected_node)

    def calculate_weight(self, node):
        return (self.blocked_cache[node] + 1)**self.heuristic_weight * self.pheromones_cache[node]**self.pheromone_weight

    def select_node(self):
        nodes = list(self.choosable)

        weights = np.array([self.calculate_weight(node) for node in nodes])
        total = weights.sum()

        if total == 0:
            return random.choice(nodes)

        weights /= total
        return nodes[np.random.choice(len(nodes), p=weights)]