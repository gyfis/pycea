from abc import ABCMeta, abstractmethod
from random import random, uniform, randrange
from copy import deepcopy


class Operator(object, metaclass=ABCMeta):
    @abstractmethod
    def operate(self, *individuals):
        pass


class Mutation(Operator):
    @abstractmethod
    def operate(self, individual):
        pass


class FlipMutation(Mutation):
    def __init__(self, mutation_probability=0.05, flip_probability=0.05):
        self.mutation_probability = mutation_probability
        self.flip_probability = flip_probability

    def operate(self, individual):
        new_individual = deepcopy(individual)

        if random() < self.mutation_probability:
            for index, value in individual.iter_values():
                if random() < self.flip_probability:
                    new_individual.values[index] = 1 - value

        return new_individual


class Crossover(Operator):
    @abstractmethod
    def operate(self, *individuals):
        pass


class PointCrossover(Crossover):
    def operate(self, *individuals):
        new_individual = deepcopy(individuals[0])
        size = individuals[0].size
        split_point = randrange(size)
        for i in range(split_point, size):
            new_individual[i] = individuals[1][i]

        return new_individual


class Selector(Operator):
    @abstractmethod
    def operate(self, *individuals):
        pass


class RouletteSelector(Selector):
    def operate(self, *individuals):

        total_fitness = sum(individual.fitness() for individual in individuals)

        selected_individuals = [None, None]
        for i in range(2):
            roulette_fitness = uniform(0, total_fitness)
            current_fitness = 0
            for individual in individuals:
                current_fitness += individual.fitness()
                if current_fitness > roulette_fitness:
                    selected_individuals[i] = deepcopy(individual)
                    break

        return selected_individuals
