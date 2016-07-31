"""

GA Base

Description Here!

    Copyright (C) 2016  Cameron Kingsbury

    This program is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later 
version.

    This program is distributed in the hope that it will be 
useful, but WITHOUT ANY WARRANTY; without even the implied 
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program.  If not, see 
<http://www.gnu.org/licenses/>.

To do:
-Comment
-Create optional constraints that are governed by fitness
-Create variable parents, unfits, and mutation probability
"""


import random
import numpy as np
from decimal import Decimal


class GeneticsLab(object):

    def __init__(self, num_inputs, fitness_function,
                 population_size, c_mag=1000, num_parents=3,
                 num_unfit=1, probability_mutate=0.1,
                 soft_constraints=None):

        self.num_inputs = num_inputs
        if soft_constraints is not None:
            self.soft_constraints = soft_constraints
        else:
            self.soft_constraints = \
                [(-c_mag, c_mag)] * num_inputs
        self.fitness_function = fitness_function
        self.population_size = population_size
        self.probability_mutate = probability_mutate
        self.fitness_dict = {}
        self.generation = -1
        self.generation_fitness = []

        self.num_parents = num_parents
        self.num_unfit = num_unfit
        self.num_fit = num_parents - num_unfit

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
            key=lambda x: self.fitness_dict[x])

        parents = self.population[:self.num_fit]
        unfit = set(self.population[self.num_fit:])
        for count in range(self.num_unfit):
            choice = random.choice(tuple(unfit))
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

        for index, attributes in enumerate(zip(
                parent_1, parent_2)):
            if random.random() < self.probability_mutate:
                child.append(self.mutate(index))
            else:
                child.append(random.choice(attributes))

        return tuple(child)

    def mutate(self, i_index):
        c_min = self.soft_constraints[i_index][0]
        c_max = self.soft_constraints[i_index][1]
        return Decimal(str(random.uniform(c_min, c_max)))

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
            self.mutate(count) for count in range(self.num_inputs))


def set_softs(c_min, c_max, count):
    return [(c_min, c_max)] * count


def rosenbrock(coords):
    x, y = coords
    return (1 - x)**2 + 100 * (y - x**2)**2
