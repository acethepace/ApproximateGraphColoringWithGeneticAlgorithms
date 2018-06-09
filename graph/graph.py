class Graph:
    no_points = 0
    no_colours = 0
    def __init__(self, points, edges):
        Graph.no_points = len(points)
        self.points = points
        self.edges = edges

    def __str__(self):
        points = '['
        for point in self.points:
            points += str(point)
        points += ']'
        edges = '['
        for edge in self.edges:
            edges += str(edge)
        edges += ']'
        return points + "\n" + edges
