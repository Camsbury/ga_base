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
        for count in self.num_unfit_parents:
            choice = random.choice(unfit)
            parents.append(choice)
            unfit.remove(choice)
        self.breed(parents)


    def breed(self, parents):
        self.population = parents
        len_population = len(parents)
        while len_population < self.population_size:
            #choose parent 1 based on fitness
            #choose parent 2 based on fitness
            #birth unique


    def gen_zero(self):

        self.create_individual = _define_individual(
self.num_inputs, self.min_value, self.max_value)

        #reformat for creating only unique individuals
        self.population = \
[self.create_individual() for count in self.population_size]


    def _define_individual(
self, num_inputs, min_value, max_value):

        def create_individual():
            return tuple(random.randint(
min_value, max_value) for count in num_inputs)

        return create_individual
