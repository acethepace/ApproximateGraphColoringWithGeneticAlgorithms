from util.params import Params
from util.util import *
from main import work

stats_dict = {}

for crossover_function in ["Standard", "Jumbled"]:
    stats_dict[crossover_function] = []

Params.mutation_function = "None"
try:
    for n in range(1, 21):
        print("iteration", n)
        n *= 5
        if n < 50:
            Params.no_colours = 5
        else:
            Params.no_colours = 8

        points = get_random_points(n)
        edges = get_random_edges(n, n)

        for crossover_function in ["Standard", "Jumbled"]:
            Params.crossover_function = crossover_function
            stats_dict[crossover_function].append(work(points, edges))
except:
    print("FAILED, big time")
    pass

for key in stats_dict.keys():
    print(key, " || ", end="")
    for stat in stats_dict.get(key):
        print(stat, "\\\\", end="")

    print()
