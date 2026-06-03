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
        self.heuristic_weight = heuristic_weight
        self.pheromone_weight = pheromone_weight


    def __str__(self):
        return f'Ant {self.ant_id}: colored {self.colored} nodes from all {self.graph.number_of_nodes()} nodes'


    def run(self):
        curr_colors = 1

        #iterujemy, dopóki są jeszcze dostępne node w zbiorze wybieralnych
        while self.colored < self.graph.number_of_nodes():
            self.create_color_subset(curr_colors)
            curr_colors += 1

        return self.colors


    def reset(self):
        self.choosable = set(node for node in self.colors.keys() if self.colors[node] is None)
        self.blocked = set()


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


    def count_blocked_neighbors(self, node):
        count = 0
        for neighbor in self.graph.neighbors(node):
            if neighbor in self.blocked:
                count += 1
        return count


    def read_pheromones(self, node, color_subset):
        pheromone = 0.0
        for colored_node in color_subset:
            pheromone += self.pheromones.get_pheromone(node, colored_node)
        pheromone /= len(color_subset)
        return pheromone


    def calculate_probability(self, node, color_subset):
        pheromone = self.read_pheromones(node, color_subset)
        blocked_neighbors = self.count_blocked_neighbors(node)
        return pheromone**self.pheromone_weight * blocked_neighbors**self.heuristic_weight


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
        self.remove_neighbors(start_node)

        while self.choosable:
            # obliczamy prawdopodobieństwo dla każdego node ze zbioru wybieralnych
            probabilities = {node: self.calculate_probability(node, color_subset) for node in self.choosable}

            # na podstawie prawdopodobieństwa losujemy node do pokolorowania
            total_probability = sum(probabilities.values())
            if total_probability == 0:
                probabilities = {node: 1.0 / len(self.choosable) for node in self.choosable}
            selected_node = random.choices(list(probabilities.keys()), weights=list(probabilities.values()), k=1)[0]

            self.colored += 1
            color_subset.add(selected_node)
            self.colors[selected_node] = color
            self.remove_neighbors(selected_node)