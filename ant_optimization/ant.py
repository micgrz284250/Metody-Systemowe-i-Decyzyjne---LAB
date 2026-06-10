import random


class Ant:
    def __init__(self, ant_id, graph, pheromones, heuristic_weight=4.0, pheromone_weight=2.0):
        self.ant_id = ant_id
        self.graph = graph
        self.pheromones = pheromones
        self.choosable = set()
        self.blocked = set()
        self.colored = 0
        self.colors = {node: None for node in self.graph.nodes}
        self.blocked_count = {node: 0 for node in self.graph.nodes}
        self.pheromones_cache = {node: 0.0 for node in self.graph.nodes}
        self.heuristic_weight = heuristic_weight
        self.pheromone_weight = pheromone_weight

    def __str__(self):
        return f'Ant {self.ant_id}: colored {self.colored} nodes from all {self.graph.number_of_nodes()} nodes'

    def run(self):
        curr_colors = 1

        #iterujemy, dopóki są jeszcze dostępne niepokolorowane node
        while self.colored < self.graph.number_of_nodes():
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

        for neighbor in self.graph.neighbors(node):
            if neighbor in self.choosable:
                self.choosable.remove(neighbor)

            if neighbor not in self.blocked:
                self.blocked.add(neighbor)

    def update_blocked_count(self, node):
        for neighbor in self.graph.neighbors(node):
            self.blocked_count[neighbor] += 1

    def update_pheromones_cache(self, node):
        for node_ in self.choosable:
            self.pheromones_cache[node] += self.pheromones.get_pheromone(node, node_)

    def update(self, node):
        self.remove_neighbors(node)
        self.update_blocked_count(node)
        self.update_pheromones_cache(node)

    def calculate_probability(self, node):
        pheromone = self.pheromones_cache[node]
        blocked_neighbors = self.blocked_count[node] + 1  # +1, aby uniknąć dzielenia przez zero
        return pheromone ** self.pheromone_weight * blocked_neighbors ** self.heuristic_weight

    def create_color_subset(self, color):
        # definiujemy sobie podzbiór node, które będą miały ten sam kolor
        color_subset = set()

        # resetujemy zbiory wybieralnych i zablokowanych
        self.reset()

        # pobieramy startowy node dla zbioru
        start_node = self.get_start_point()
        self.colored += 1
        color_subset.add(start_node)
        self.colors[start_node] = color

        # usuwamy sąsiadów startowego node ze zbioru wybieralnych
        self.update(start_node)

        while self.choosable:
            # obliczamy prawdopodobieństwo dla każdego node ze zbioru wybieralnych
            probabilities = {node: self.calculate_probability(node) for node in self.choosable}

            # na podstawie prawdopodobieństwa losujemy node do pokolorowania
            total_probability = sum(probabilities.values())
            if total_probability == 0:
                probabilities = {node: 1.0 / len(self.choosable) for node in self.choosable}
            selected_node = random.choices(list(probabilities.keys()), weights=list(probabilities.values()), k=1)[0]

            self.colored += 1
            color_subset.add(selected_node)
            self.colors[selected_node] = color
            self.update(selected_node)
