from individuals import BinaryIndividual
from neighborhoods import LinearNeighborhood
from operators import FlipMutation, RouletteSelector, PointCrossover
from random import randrange
import matplotlib.pyplot as plt
from matplotlib import animation, colors
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import logging


class CEA(object):
    class Grid(object):
        def __init__(self, individual=BinaryIndividual, grid_size=(15, 15)):
            self.grid_size = grid_size
            self.individual = individual
            self.grid = [[individual(i, j, grid_size[0], grid_size[1]) for j in range(grid_size[1])]
                         for i in range(grid_size[0])]
            self.new_population_grid = [[individual(i, j, grid_size[0], grid_size[1]) for j in range(grid_size[1])]
                                        for i in range(grid_size[0])]

        def get_individual(self, loc):
            return self.grid[loc[0]][loc[1]]

        def set_individual(self, loc, individual):
            self.grid[loc[0]][loc[1]] = individual

        def set_new_individual(self, loc, individual):
            self.new_population_grid[loc[0]][loc[1]] = individual

        def merge_new_population(self):
            #  possibility to implement some sort of elitism here
            temp_grid = self.grid
            self.grid = self.new_population_grid
            self.new_population_grid = temp_grid

        def get_fitness(self):
            return sum(individual.fitness() for _, _, individual in self.grid_iter())

        def get_objective(self):
            return sum(individual.objective() for _, _, individual in self.grid_iter())

        def get_neighbors(self, neighborhood):
            return [self.get_individual((x, y)) for (x, y) in neighborhood]

        def get_heat_data(self):
            return np.array([[self[i, j].fitness() / self[i, j].size for j in range(self.grid_size[1])] for i in range(self.grid_size[0])])
            # heatmap_array = np.ndarray(self.grid_size)
            # for i in range(self.grid_size[0]):
            #     for j in range(self.grid_size[1]):
            #         heatmap_array[i, j] = self[i, j].fitness() / self[i, j].size
            # return heatmap_array
            # return np.array([individual.fitness() / individual.size for _, _, individual in self.grid_iter()])

        def __getitem__(self, loc):
            return self.get_individual(loc)

        def __setitem__(self, loc, individual):
            self.set_individual(loc, individual)

        def grid_iter(self):
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    yield i, j, self[i, j]

        def random_access(self):
            x, y = randrange(0, self.grid_size[0]), randrange(0, self.grid_size[1])
            return x, y, self[x, y]

    def __init__(self, individual=BinaryIndividual, grid_size=(30, 30)):
        self.neighborhood = LinearNeighborhood(distance=2)
        self.mutation = FlipMutation()
        self.crossover = PointCrossover()
        self.selector = RouletteSelector()

        self.operators = [self.selector, self.crossover]

        self.grid = CEA.Grid(individual, grid_size)

    def iterate_population(self):
        for i, j, _ in self.grid.grid_iter():
            self.evolve_individual(i, j, new=True)

        self.grid.merge_new_population()

        logging.info('Objective: {0}'.format(self.grid.get_objective()))

    def iterate_individual(self):
        i, j, _ = self.grid.random_access()
        self.evolve_individual(i, j, new=False)

        logging.info('Objective: {0}'.format(self.grid.get_objective()))

    def evolve_individual(self, i, j, new=True):
        new_individual = self.grid.get_neighbors(self.neighborhood.neighborhood((i, j), self.grid.grid_size))
        for op in self.operators:
            if isinstance(new_individual, BinaryIndividual):
                new_individual = op.operate(new_individual)
            else:
                new_individual = op.operate(*new_individual)

        if new:
            self.grid.set_new_individual((i, j), new_individual)
        else:
            self.grid[i, j] = new_individual


def heatmap(cea, synchronous=True):
    data = cea.grid.get_heat_data()
    fig, ax = plt.subplots()
    cmap = LinearSegmentedColormap.from_list('my cmap', ['black', 'white'])
    heatmap_plot = ax.imshow(data, interpolation='nearest', cmap=cmap, vmin=0, vmax=1.0)

    def init():
        heatmap_plot.set_data(cea.grid.get_heat_data())
        return heatmap_plot

    def animate(i):
        if i > 2:
            cea.iterate_population() if synchronous else cea.iterate_individual()
        heatmap_plot.set_data(cea.grid.get_heat_data())
        return heatmap

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=150)

    plt.axis('off')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    anim.save('gifs/slash_final.gif', writer='imagemagick')

    plt.show()


def synchronous_cea():
    cea = CEA(grid_size=(100, 100))
    heatmap(cea)


def asynchronous_cea():
    cea = CEA(grid_size=(100, 100))
    heatmap(cea, synchronous=False)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    synchronous_cea()
