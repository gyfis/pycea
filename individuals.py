from abc import ABCMeta, abstractmethod
from random import randint


class Individual(object, metaclass=ABCMeta):
    @abstractmethod
    def iter_values(self):
        pass

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def objective(self):
        pass


class BinaryIndividual(Individual):
    def __init__(self, i, j, max_i, max_j, size=20):
        self.i = i
        self.j = j
        self.size = size
        self.values = [0]*size if i != j else [1]*size
        # self.values = [0]*size if i != 0 and j != 0 and i != max_i - 1 and j != max_j - 1 else [1]*size  # [randint(0, 1) for _ in range(size)]
        # self.values = [0]*size if i != max_i // 2 and j != max_j // 2 else [1]*size
        # self.values = [0]*size if i != 0 and i != max_i - 1 else [1]*size

    def iter_values(self):
        for index, value in enumerate(self.values):
            yield index, value

    def fitness(self):
        return sum(self.values) + 1

    def objective(self):
        return self.size - sum(self.values)

    def get_value(self, index):
        return self.values[index]

    def set_value(self, index, value):
        self.values[index] = value

    def __getitem__(self, index):
        return self.get_value(index)

    def __setitem__(self, index, value):
        self.set_value(index, value)


class FunctionIndividual(Individual):
    def __init__(self, function, size=20):
        self.function = function
        self.values = [randint(0, 1) for _ in range(size)]
        self.size = size

    def iter_values(self):
        for index, value in enumerate(self.values):
            yield index, value

    def fitness(self):
        return self.function(int(''.join(map(str, self.values)), 2))

    def objective(self):
        return self.size - self.fitness()

    def get_value(self, index):
        return self.values[index]

    def set_value(self, index, value):
        self.values[index] = value

    def __getitem__(self, index):
        return self.get_value(index)

    def __setitem__(self, index, value):
        self.set_value(index, value)