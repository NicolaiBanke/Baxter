from baxter.strategy.strategy import Strategy
from baxter.backtest import Backtest

def attatch_strategy(strategy: Strategy) -> None:
    if not isinstance(strategy, Strategy):
        return TypeError("A Strategy object must be passed")
    else:
        Backtest.strategy = strategy