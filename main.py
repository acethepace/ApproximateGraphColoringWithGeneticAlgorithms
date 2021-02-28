from random import choice
from time import clock
from time import sleep

import matplotlib

from genetic.gene import Gene
from genetic.population import Population
from graph.graph import Graph
from util.Stats import Stats
from util.params import Params
from util.util import get_random_points, get_random_edges

matplotlib.use("TkAgg")

graph = None
no_points = 0


def get_random_parent(no_colours, no_points):
    sample_numbers = []
    for i in range(no_points):
        sample_numbers.append(int(choice(range(no_colours))))
    sample_numbers[0] = 0
    return Gene(sample_numbers)


def initialize_population():
    n = Params.initial_population_size
    population = []
    for i in range(n):
        population.append(get_random_parent(Graph.no_colours, no_points))
    return Population(population)


def plot_figure(gene, graph):
    subplot = Params.subplot
    if subplot is None or Params.root is None or Params.canvas is None:
        return
    subplot.clear()
    default_color = 'kx'
    color_map = {0: 'go', 1: 'bo', 2: 'ro', 3: 'yo', 4: 'mo', 5: 'co', 6: 'ko'}
    colors_list = []
    for i in gene.array:
        if i in color_map:
            colors_list.append(color_map[i])
        else:
            colors_list.append(default_color)

    for i in range(len(graph.points)):
        subplot.plot(graph.points[i].x, graph.points[i].y, colors_list[i])

    for edge in graph.edges:
        subplot.plot([graph.points[edge.start].x, graph.points[edge.end].x], [graph.points[edge.start].y,
                                                                              graph.points[edge.end].y], 'k-')

    Params.root.update()
    Params.canvas.draw()
    sleep(Params.display_delay)


def do_genetic(population, population_propogation_function):
    iterations = 0
    last_n = [float('Inf')] * Params.stop_genetic_after_count
    best_gene = None
    while True:
        iterations += 1
        max_evaluation = population.get_max_evaluation(graph)
        last_n.pop(0)
        last_n.append(max_evaluation)
        flag = False
        for i in range(len(last_n)):
            if i != 0 and last_n[i] != last_n[i - 1]:
                flag = True
        if not flag:
            break
        print(max_evaluation)
        best_gene = population.best_n(1, graph)[0]
        print(best_gene)
        if Params.show_plot:
            plot_figure(best_gene, graph)
        new_population = population_propogation_function(population, graph)
        population = Population(new_population)
    Graph.no_colours = len(set(best_gene.array))
    eval = best_gene.evaluate(graph)
    no_colors = len(set(best_gene.array))
    conflicts = -1 * (eval + (no_colors * Params.penalty_per_color_used)) / Params.penalty_same_color

    return iterations, best_gene, conflicts


def population_propogation_default(population, graph):
    parents_crossover = population.best_n(Params.crossover_parents, graph)
    parents_mutation = population.best_n(Params.mutation_parents, graph)
    new_population = []
    new_population.extend(population.best_n(Params.propogation_count, graph))
    new_population.extend(population.crossover(parents_crossover))
    new_population.extend(population.mutate(parents_mutation, graph))
    new_population.extend(population.random(Params.random_count))
    return new_population


def work(points, edges):
    t1 = clock()
    global no_points
    no_points = len(points)
    global graph
    graph = Graph(points, edges)
    no_colours = Params.no_colours
    Graph.no_colours = no_colours
    population = initialize_population()
    iterations, best_gene, conflicts = do_genetic(population, population_propogation_default)
    time = clock() - t1
    colors_used = Graph.no_colours
    return Stats(iterations, time, colors_used, best_gene, conflicts, graph)


# work(get_random_points(10), get_random_edges(10, 10))




# print('DONE!')

# root.mainloop()
