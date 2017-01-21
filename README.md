pywarships
==========

`pywarships` is a library that can simulate the results of playing Warships with some strategy. It generates data that can be plotted to show the probability curve of winning the game in some number of moves.

Included strategies
-------------------

The strategies that are included with library are `RandomStrategy`, `HumanStrategy` and `AnalyticalStrategy` - all in the `strategies` module.
These are the most common strategies that come to mind when plaing Warships - see if you can come up with a better strategy!

How to make my own strategies?
------------------------------

If you want, you can create your own strategy - it must be child of the `strategies.strategy.Strategy` class and implement the `run` method:

```python
def run(self, grid: Grid):
    # your code goes here
```

How to test my strategies?
--------------------------

Simply use the `engine.strategy_tester.StrategyTester` class. It has got a constructor with one optional argument - the number of workers assigned to complete the computation. Workers are different processes, running in parallel - If you are on a `x` core proccesor, to be most efficient you can set the number of workers to `x`. The default is one worker. `StrategyTester` has 3 main testing methods - `test`, `test_to_console` and `test_to_file`:

```python
test(strategy: Strategy, num_of_games)
test_to_console(strategy: Strategy, num_of_games)
test_to_file(strategy: Strategy, num_of_games, filename: str)
```

`test` just runs the simulation `num_of_games` times and returns a `(wins, cumulative_probabilities)` tuple, where `wins[x]` is a number representing the amount of wins at `x` moves (from 0 to 100), and `cumulative_probabilities` is an list of ready-to-plot values representing the cumulative probability curve.

`test_to_console` displays the progress of the computation in the console and prints out the `wins` and `cumulative_probabilities` lists.

`test_to_file` runs simulation the same way that the `test` function does, and saves the results in `filename`.

**Example of test:**

```python
from engine.strategy_tester import StrategyTester
from strategies.random_strategy import RandomStrategy

if __name__ == "__main__":
    num_of_games = 10**5

    st = StrategyTester(4)
    st.test_to_console(RandomStrategy(), num_of_games)
```

How to create my own ship configurations?
-----------------------------------------

You can do this by using the `ShipConfig` class from `engine.warships`. Example:

```python
def create_my_great_config():
    from engine.warships import ShipConfig

    config = ShipConfig()
    ships = {1: 2, 3: 1, 5: 2, 7: 1}

    for length, quantity in zip(ships.keys(), ships.values()):
        config.add_ship_details(length, quantity)

    # Oh, I forgot, I wanted 3 ships of length 1... Luckily, I can fix this:
    config.add_ship_of_length(1)

    return config
```

And then, you can use the previously created config to simulate games with it:

```python

from engine.strategy_tester import StrategyTester
from strategies.random_strategy import RandomStrategy

if __name__ == "__main__":
    num_of_games = 10**5

    st = StrategyTester(4, create_my_great_config())
    st.test_to_console(RandomStrategy(), num_of_games)

```
