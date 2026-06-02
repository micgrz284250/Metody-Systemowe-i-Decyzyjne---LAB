import random

from networkx.classes import graph

from ant_optimization.pheromones import Pheromones


class Ant:
    def __init__(self, ant_id, graph):
        self.ant_id = ant_id
        self.graph = graph
        self.pheromones = Pheromones(graph)
        self.choosable = set(graph.nodes())
        self.blocked = set()
        self.colors = {node: None for node in graph.nodes()}


    def run(self):
        curr_colors = 1

        #iterujemy, dopóki są jeszcze dostępne node w zbiorze wybieralnych
        while self.choosable:
            # resetujemy zbiory wybieralnych i zablokowanych
            self.reset()

            # pobieramy startowy node dla zbioru
            start_node = self.get_start_point()

            # usuwamy sąsiadów startowego node ze zbioru wybieralnych
            self.remove_neighbors(start_node)



            # koniec tworzenia danego zbioru, zwiększamy kolor
            curr_colors += 1


    def get_start_point(self):
        return random.choice(list(self.choosable))

    def remove_neighbors(self, node):
        if node in self.choosable:
            self.choosable.remove(node)

        if node not in self.blocked:
            self.blocked.add(node)

        for neighbor in self.graph.neighbors(node):
            if neighbor in self.choosable:
                self.choosable.remove(neighbor)

            if neighbor not in self.blocked:
                self.blocked.add(neighbor)

    def reset(self):
        self.choosable = set()
        self.blocked = set()
        for node in self.graph.nodes():
            if node in self.colors.keys():
                self.choosable.add(node)
            else:
                self.blocked.add(node)