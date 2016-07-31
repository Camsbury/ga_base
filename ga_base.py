import random
import numpy as np



class GeneticsLab(object):

    def __init__(self, num_inputs, min_value, max_value, \
fitness_function, population_size, percent_parents = 0.2, \
percent_unfit = .05, percent_mutate = 0.01):


    self.num_inputs = num_inputs
    self.min_value = min_value
    self.max_value = max_value
    self.fitness_function = fitness_function
    self.population_size = population_size
    self.percent_parents = percent_parents
    self.percent_unfit = percent_unfit
    self.percent_mutate = percent_mutate
    self.generations = generations
    self.fitness_dict = {}
    self.generation = 0
    self.generation_fitness = []

    self.create_individual = \
_define_individual(num_inputs, min_value, max_value)

    self.population = \
[self.create_individual() for count in self.population_size]

    self.num_parents = \
round(self.percent_parents * self.population_size)

    self.num_unfit_parents = \
round(self.percent_unfit * self.num_parents)

    self.num_fit_parents = \
self.num_parents - self.num_unfit_parents



    def evolve(self):
        pass


    def _define_individual(
self, num_inputs, min_value, max_value):

        def create_individual():
            return tuple(random.randint(
min_value, max_value) for count in num_inputs)

        return create_individual
