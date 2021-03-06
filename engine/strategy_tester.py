from engine import warships as WS
from engine.warships import ShipConfig
from strategies.strategy import Strategy
from multiprocessing import Pool
from copy import deepcopy


class Iterator:
    def __init__(self, count, strategy, config):
        self.counter = count
        self.strategy = strategy
        self.config = config

    def __iter__(self):
        return self

    def __next__(self):
        self.counter -= 1
        if self.counter >= 0:
            return self.strategy(), deepcopy(self.config)
        else:
            raise StopIteration


def worker1(params):
    strategy, config = params
    grid = WS.gen_rand_grid(config)

    while not grid.is_won():
        strategy.run(grid)

    return grid.checked_cells


class StrategyTester:
    def __init__(self, workers=1, config=ShipConfig("polish")):
        self.workers = workers
        self.config = config

    def test_to_console(self, strategy: Strategy, num_of_games):
        wins = [0 for i in range(101)]
        with Pool(self.workers) as p:
            j = 0
            for i in p.imap_unordered(worker1, Iterator(num_of_games, type(strategy), self.config)):
                j += 1
                wins[i] += 1
                won_games = "Won {} game out of {} games".format(j, num_of_games)
                percentage = "[{:.2%}]".format((j) / num_of_games)
                numspace = 45 - (len(won_games) + len(percentage))
                print("\r" + won_games + " " * numspace + percentage, end="")

        probabilities = self.__wins_to_cumulative_probability(wins, num_of_games)
        print("\nList of wins:")
        print(wins)
        print("List of cumulative probabilities of winning at some number of moves:")
        print(probabilities)

    def test_to_file(self, strategy: Strategy, num_of_games, filename):
        wins = [0 for i in range(101)]
        with Pool(self.workers) as p:
            j = 0
            for i in p.imap_unordered(worker1, Iterator(num_of_games, type(strategy), self.config)):
                j += 1
                wins[i] += 1

        probabilities = self.__wins_to_cumulative_probability(wins, num_of_games)
        file = open(filename, "w")
        file.writelines((str(wins), "\n", str(probabilities)))
        file.close()

    def test(self, strategy: Strategy, num_of_games):
        wins = [0 for i in range(101)]
        with Pool(self.workers) as p:
            j = 0
            for i in p.imap_unordered(worker1, Iterator(num_of_games, type(strategy), self.config)):
                j += 1
                wins[i] += 1
        probabilities = self.__wins_to_cumulative_probability(wins, num_of_games)
        return wins, probabilities

    def __wins_to_cumulative_probability(self, wins, num_of_games):
        probability = []
        current_probability = 0
        for item in wins:
            if item != 0:
                current_probability += item / num_of_games
            probability.append(current_probability)
        return probability
