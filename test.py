from engine.strategy_tester import StrategyTester
from strategies.human_strategy import HumanStrategy
from strategies.random_strategy import RandomStrategy
from strategies.analytical_strategy import AnalyticalStrategy


if __name__ == "__main__":
    num_of_games = 10**4

    st = StrategyTester(8)
    st.test_to_console(RandomStrategy(), num_of_games) # Hey, it's working!
