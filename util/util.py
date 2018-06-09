import random

from graph.edge import Edge
from graph.point import Point


def get_random_points(no_points):
    points = []
    i = 0
    while i < no_points:

        x = random.randint(0, 100)
        y = random.randint(0, 100)
        new_point = Point(x, y)
        for point in points:
            if str(point) == str(new_point):
                continue
        points.append(new_point)
        i += 1
    # print('random points: ' + points)
    return points


def get_random_edges(no_points, no_edges):
    edges = []
    i = 0
    while i < no_edges:
        start = random.randint(0, no_points - 1)
        end = random.randint(0, no_points - 1)
        new_edge = Edge(start, end)
        for edge in edges:
            if str(edge) == str(new_edge):
                continue
        edges.append(new_edge)
        i += 1
    # print('random edges : ' + edges)
    return edges
