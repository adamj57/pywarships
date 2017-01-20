pywarships
==========

`pywarships` is a library that can simulate results playing warships game with some strategies. It generates data that can be plotted to show probability curve of winning the game in some number of moves.

Included strategies
-------------------

The strategies that are included with library are `RandomStrategy`, `HumanStrategy` and `AnalyticalStrategy` - all in `strategies` module.
These are the moste common strategies to think about when it comes to plaing warships - see if you can come up with better strategy!

How to make my own strategies?
------------------------------

If you want, you can create your own strategy - it must be child of `strategies.strategy.Strategy` class and implement `run` method:

```python
def run(self, grid: Grid):
    # your code goes here
```

How to test my strategies?
--------------------------

Simply, use `engine.strategy_tester.StrategyTester` class. It has constructor with one optional argument - the number of workers assigned to complete the computation. Workers are different processes, running in parallel - If you are on `x` core proccesor, to be most efficient you can set number of workers to `x`. `StrategyTester` has 3 main testing methods - `test`, `test_to_console` and `test_to_file`:

```python
test(strategy: Strategy, num_of_games)
test_to_console(strategy: Strategy, num_of_games)
test_to_file(strategy: Strategy, num_of_games, filename: str)
```

`test` just runs simulation `num_of_games` times and returns `(wins, cumulative_probabilities)` tuple, where `wins[x]` is number representing wins count at `x` moves (`x` from 0 to 100), and `cumulative_probabilities` is an list of ready-to-plot values representing cumulative probability curve.

`test_to_console` displays progress of computing in console and prints out `wins` and `cumulative_probabilities` lists.

`test_to_file` runs simulation as in `test` function and saves results in `filename`.

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

You can do this by using `ShipConfig` class from `engine.warships`. Example:

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

And then, you can use previously created config to simulate games with it:

```python

from engine.strategy_tester import StrategyTester
from strategies.random_strategy import RandomStrategy

if __name__ == "__main__":
    num_of_games = 10**5

    st = StrategyTester(4, create_my_great_config())
    st.test_to_console(RandomStrategy(), num_of_games)

```