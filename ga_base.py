import random
import numpy as np



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

    self.num_parents = \
round(percent_parents * self.population_size)

    self.num_unfit_parents = \
round(percent_unfit * self.num_parents)

    self.num_fit_parents = \
self.num_parents - self.num_unfit_parents


    def evolve(self):

        if self.generation == -1:
            gen_zero(self)
        else:
            breed(self)

        self.generation += 1


    def breed(self):
        parents.sort(key = lambda x: self.fitness_dict[x])
        parents = self.population[:self.num_fit_parents]
        unfit = set(self.population[self.num_fit_parents:])
        for count in self.num_unfit_parents:
            choice = random.choice(unfit)
            parents.append(choice)
            unfit.remove(choice)

    def gen_zero(self):

        self.create_individual = _define_individual(
self.num_inputs, self.min_value, self.max_value)

        self.population = \
[self.create_individual() for count in self.population_size]


    def _define_individual(
self, num_inputs, min_value, max_value):

        def create_individual():
            return tuple(random.randint(
min_value, max_value) for count in num_inputs)

        return create_individual
