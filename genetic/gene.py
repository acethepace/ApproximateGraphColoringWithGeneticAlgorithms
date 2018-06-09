import operator
from random import randint

from graph.graph import Graph
from util.params import Params


def swap(array, i, j):
    arr2 = array[:]
    arr2[i], arr2[j] = arr2[j], arr2[i]
    return arr2


def get_any_wrongly_colored_node(arr, graph):
    for edge in graph.edges:
        if arr[edge.start] == arr[edge.end]:
            return edge.start
    return 1


def get_worst_placed_node(arr, graph):
    scores_dict = {}
    for edge in graph.edges:
        if arr[edge.start] == arr[edge.end]:
            if edge.start in scores_dict:
                scores_dict[edge.start] += 1
            else:
                scores_dict[edge.start] = 1

            if edge.end in scores_dict:
                scores_dict[edge.end] += 1
            else:
                scores_dict[edge.end] = 1
    try:
        return max(scores_dict.items(), key=operator.itemgetter(1))[0]
    except ValueError:
        return randint(0, len(graph.points) - 1)


def get_final_color(worst_pos, array, graph):
    connected_nodes = []
    for edge in graph.edges:
        if edge.start == worst_pos:
            connected_nodes.append(edge.end)
        if edge.end == worst_pos:
            connected_nodes.append(edge.start)

    colors_dict = {}
    for i in range(Graph.no_colours):
        colors_dict.update({i: 0})

    for node in connected_nodes:
        colors_dict[array[node]] += 1

    return max(colors_dict.items(), key=operator.itemgetter(1))[0]


class Gene:
    def __init__(self, array):
        self.array = array  # will be an array of size no_points with each element being the color for
        # point at that position

    def reproduce(self, obj2):
        part_a = []
        part_b = []

        for i in range(Graph.no_points):
            if i < Graph.no_points / 2:
                part_a.append(self.array[i])
            else:
                part_b.append(obj2.array[i])

        progeny = []
        for i in range(Graph.no_points):
            if i < Graph.no_points / 2:
                progeny.append(part_a.pop(0))
            else:
                progeny.append(part_b.pop(0))
        return Gene(progeny)

    def reproduce_1(self, obj2):
        progeny = []
        for i in range(Graph.no_points):
            if i % 2 == 0:
                progeny.append(self.array[i])
            else:
                progeny.append(obj2.array[i])
        return Gene(progeny)

    def evaluate(self, graph):
        evaluation = 0.0
        for edge in graph.edges:
            if self.array[edge.start] == self.array[edge.end] and edge.start != edge.end:
                evaluation += Params.penalty_same_color

        evaluation += len(set(self.array)) * Params.penalty_per_color_used
        self.evaluation = -1 * evaluation
        return -1 * evaluation

    def mutate(self, graph=None):
        i = randint(1, len(self.array) - 1)
        j = randint(1, len(self.array) - 1)
        return Gene(swap(self.array, i, j))

    def mutate_1(self, graph):
        worst_pos = get_worst_placed_node(self.array, graph)
        final_color = get_final_color(worst_pos, self.array, graph)
        self.array[worst_pos] = final_color
        new_arr = self.array[:]
        new_arr[worst_pos] = final_color
        return Gene(new_arr)

    def mutate_2(self, graph):
        worst_pos = get_worst_placed_node(self.array, graph)
        new_arr = self.array[:]
        new_arr[worst_pos] = randint(0, Graph.no_colours)
        return Gene(new_arr)

    def mutate_3(self, graph):
        pos = get_any_wrongly_colored_node(self.array, graph)
        new_arr = self.array[:]
        new_arr[pos] = get_final_color(pos, self.array, graph)
        return Gene(new_arr)

    def mutate_4(self, graph):
        pos = get_any_wrongly_colored_node(self.array, graph)
        new_arr = self.array[:]
        new_arr[pos] = randint(0, Graph.no_colours)
        return Gene(new_arr)

    def __str__(self):
        return str(self.array)
