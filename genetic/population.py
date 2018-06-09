from random import choice

from genetic.gene import Gene
from graph.graph import Graph
from util.params import Params


class Population:
    def __init__(self, genes, mutation_count=1000, crossover_count=1000, random_count=100):
        self.genes = genes
        self.mutation_count = mutation_count
        self.crossover_count = crossover_count
        self.random_count = random_count

    def best_n(self, n, graph):
        gene_scores = {}
        for gene in self.genes:
            gene_scores.update({gene: gene.evaluate(graph)})
        sorted_genes = sorted(gene_scores, key=gene_scores.get)
        best_n = sorted_genes[-1 * n:]
        if self.get_max_evaluation(graph) > Population(best_n).get_max_evaluation(graph):
            print('ERROR')
        return best_n

    @staticmethod
    def crossover(parents):
        children = []
        for papa in parents:
            for mummy in parents:
                if not mummy == papa:
                    if Params.crossover_function == "Standard":
                        baccha = mummy.reproduce(papa)
                    elif Params.crossover_function == "Jumbled":
                        baccha = mummy.reproduce_1(papa)
                    elif Params.crossover_function == "None":
                        return []
                    else:
                        print("unknown method : " + Params.crossover_function)
                    children.append(baccha)
        return children

    @staticmethod
    def mutate(parents, graph):
        mutation_function = Params.mutation_function

        children = []
        for parent in parents:
            if mutation_function == "Swapping":
                children.append(parent.mutate())
            elif mutation_function == "1":
                children.append(parent.mutate_1(graph))
            elif mutation_function == "2":
                children.append(parent.mutate_2(graph))
            elif mutation_function == "3":
                children.append(parent.mutate_3(graph))
            elif mutation_function == "4":
                children.append(parent.mutate_4(graph))
            elif mutation_function == "None":
                return []
            else:
                print("unknown method : " + mutation_function)
        return children

    def random(self, random_count):
        children = []
        for i in range(random_count):
            children.append(self.get_random_parent())
        return children

    def get_random_parent(self):
        sample_numbers = []
        for i in range(Graph.no_points):
            sample_numbers.append(int(choice(range(Graph.no_colours))))
        sample_numbers[0] = 0
        return Gene(sample_numbers)

    def get_max_evaluation(self, graph):
        max_evaluation = -1 * float("Inf")
        for gene in self.genes:
            if gene is None:
                self.genes.remove(gene)
            elif gene.evaluate(graph) > max_evaluation:
                max_evaluation = gene.evaluate(graph)
        return max_evaluation
