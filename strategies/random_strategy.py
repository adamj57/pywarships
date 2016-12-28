import random

from engine.warships import GridPoint
from strategies.strategy import Strategy


class RandomStrategy(Strategy):

    def run(self, grid):
        while not grid.is_won():
            coords = GridPoint(random.randint(0, 9), random.randint(0, 9))
            if not grid.is_checked(coords):
                grid.check(coords)
