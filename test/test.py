from engine.strategy_tester import StrategyTester
from strategies.human_strategy import HumanStrategy
from strategies.random_strategy import RandomStrategy
from strategies.analytical_strategy import AnalyticalStrategy


num_of_games = 10**2

st = StrategyTester()
st.test(AnalyticalStrategy(), num_of_games) # Hey, it's working!
