class Heuristica:
    def __init__(self):
        self.graph = {
            'A': [('B', 7), ('C', 9), ('D', 8), ('E', 20)],
            'B': [('A', 7), ('C', 10), ('D', 4), ('E', 11)],
            'C': [('A', 9), ('B', 10), ('D', 15), ('E', 5)],
            'D': [('A', 8), ('B', 4), ('C', 15), ('E', 17)],
            'E': [('A', 20), ('B', 11), ('C', 5), ('D', 17)],
        }
        self.ordered_edges = self.order_edges()

    def order_edges(self):
        edges = []
        visited = set()

        for origin, connections in self.graph.items():
            for destination, weight in connections:
                if (destination, origin) not in visited:
                    edges.append((origin, destination, weight))
                    visited.add((origin, destination))

        return sorted(edges, key=lambda x: x[2])

    def find(self, parent, city):
        if parent[city] != city:
            parent[city] = self.find(parent, parent[city])
        return parent[city]

    def union(self, parent, rank, city1, city2):
        root1 = self.find(parent, city1)
        root2 = self.find(parent, city2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    def heuristic(self):
        route = []
        parent = {city: city for city in self.graph}
        rank = {city: 0 for city in self.graph}
        visited_cities = set()

        for origin, destination, weight in self.ordered_edges:
            if (self.find(parent, origin) != self.find(parent, destination) and
                    (origin not in visited_cities or destination not in visited_cities)):

                route.append((origin, destination, weight))
                visited_cities.add(origin)
                visited_cities.add(destination)
                self.union(parent, rank, origin, destination)

                if len(route) == len(self.graph) - 1:
                    break

        return route


if __name__ == '__main__':
    heuristica = Heuristica()
    print(heuristica.heuristic())
