from engine import warships as WS
from engine.warships import ShipConfig
from strategies.strategy import Strategy
import time
import functools


def worker(strategy):
    strategy = type(strategy)()

class StrategyTester:
    def test(self, strategy: Strategy, num_of_games):
        wins = [0 for i in range(101)]

        for i in range(num_of_games):
            grid = WS.gen_rand_grid(ShipConfig("polish"))
            while not grid.is_won():
                strategy.run(grid)
            wins[grid.checked_cells] += 1

            won_games = "Won {} game out of {} games".format(i + 1, num_of_games)
            percentage = "[{:.2%}]".format((i + 1) / num_of_games)
            numspace = 45 - (len(won_games) + len(percentage))
            print("\r" + won_games + " " * numspace + percentage, end="")

        probabilities = self.__wins_to_cumulative_probability(wins, num_of_games)
        print("\nList of wins:")
        print(wins)
        print("List of cumulative probabilities of winning at some number of moves:")
        print(probabilities)

    def __wins_to_cumulative_probability(self, wins, num_of_games):
        probability = []
        current_probability = 0
        for item in wins:
            if item != 0:
                current_probability += item / num_of_games
            probability.append(current_probability)
        return probability
