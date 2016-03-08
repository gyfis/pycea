from abc import ABCMeta, abstractmethod


class Neighborhood(object, metaclass=ABCMeta):
    def __init__(self, distance=1):
        self.distance = distance

    @abstractmethod
    def neighborhood(self, loc, grid_size):
        pass


class LinearNeighborhood(Neighborhood):
    def neighborhood(self, loc, grid_size):
        x, y = loc

        neighborhood = [(x, y)]  # < ^ > v

        for d in range(4):
            for i in range(1, self.distance):
                if d == 0 and x >= i:
                    neighborhood.append((x - i, y))
                elif d == 1 and y >= i:
                    neighborhood.append((x, y - i))
                elif d == 2 and x + i < grid_size[0]:
                    neighborhood.append((x + i, y))
                elif d == 3 and y + i < grid_size[1]:
                    neighborhood.append((x, y + i))

        return neighborhood


class DiamondNeighborhood(Neighborhood):
    def neighborhood(self, loc, grid_size):
        x, y = loc

        neighborhood = []
        return neighborhood


class CompactNeighborhood(Neighborhood):
    def neighborhood(self, loc, gird_size):
        neighborhood = []
        return neighborhood
