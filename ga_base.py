import random
import numpy as np
from decimal import Decimal


class GeneticsLab(object):

    def __init__(self, num_inputs, min_value, max_value, \
fitness_function, population_size, percent_parents = 0.2, \
percent_unfit = .05, probability_mutate = 0.01):

        self.num_inputs = num_inputs
        self.min_value = min_value
        self.max_value = max_value
        self.fitness_function = fitness_function
        self.population_size = population_size
        self.probability_mutate = probability_mutate
        self.fitness_dict = {}
        self.generation = -1
        self.generation_fitness = []

        self.num_parents = round(
percent_parents * self.population_size)

        self.num_unfit_parents = round(
percent_unfit * self.num_parents)

        self.num_fit_parents = \
self.num_parents - self.num_unfit_parents


    def evolve_cycles(self, cycles):
        for cycle in range(cycles):
            self.evolve()


    def evolve(self):

        if self.generation == -1:
            self.gen_zero()
        else:
            self.next_gen()

        self.generation += 1
        self.measure_fitness()


    def measure_fitness(self):

        fitnesses = []
        min_fitness = float('inf')
        self.fitness_dict = {}

        for individual in self.population:
            fitness = self.fitness_function(individual)
            self.fitness_dict[individual] = fitness
            fitnesses.append(fitness)
            if fitness < min_fitness:
                min_fitness = fitness
                most_fit = individual
        self.most_fit = most_fit
        self.min_fitness = min_fitness
        self.generation_fitness.append(
np.mean(fitnesses))


    def next_gen(self):

        self.population.sort(
key = lambda x: self.fitness_dict[x])

        parents = self.population[:self.num_fit_parents]
        unfit = set(self.population[self.num_fit_parents:])
        for count in range(self.num_unfit_parents):
            choice = random.choice(unfit)
            parents.append(choice)
            unfit.remove(choice)
        self.breed(parents)


    def breed(self, parents):

        self.population = parents[:]
        len_population = len(parents)
        while len_population < self.population_size:
            fed_parents = parents[:]
            parent_1 = self.choose_parent(fed_parents)
            fed_parents.remove(parent_1)
            parent_2 = self.choose_parent(fed_parents)
            individual = self.birth(parent_1, parent_2)
            if individual not in self.population:
                self.population.append(individual)
                len_population += 1


    def birth(self, parent_1, parent_2):

        child = []

        for attributes in zip(parent_1, parent_2):
            if random.random() < self.probability_mutate:
                child.append(self.mutate())
            else:
                child.append(random.choice(attributes))
        
        return tuple(child)


    def mutate(self):
        return Decimal(str(
random.uniform(self.min_value, self.max_value)))


    def choose_parent(self, parents):

        parent_chooser = self.probabilitize(parents)
        outcome = random.random()
        for pair in parent_chooser:
            if outcome > pair[0]:
                return pair[1]
        return parent_chooser[-1][1]


    def probabilitize(self, parents):

        parent_chooser = []
        fitness_total = Decimal('0')
        for parent in parents:
            fitness = Decimal(str(
self.fitness_dict[parent]))
            parent_chooser.append([fitness, parent])
            fitness_total += fitness

        current_prob = Decimal('0')
        for index, pair in enumerate(parent_chooser):
            prob = pair[0] / fitness_total
            current_prob += prob
            pair[0] = current_prob

        return parent_chooser

    def gen_zero(self):

        self.population = []
        pop_set = set()
        current_size = 0
        while current_size < self.population_size:
            individual = self.create_individual()
            if individual not in pop_set:
                self.population.append(individual)
                pop_set.add(individual)
                current_size += 1


    def create_individual(self):

        return tuple(
self.mutate() for count in range(self.num_inputs))
