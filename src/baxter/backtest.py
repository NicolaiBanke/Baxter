from baxter.strategy.strategy import Strategy
from dataclasses import dataclass

@dataclass
class Backtest(object):
    """
    Docstring for Backtest

    This object should hold all the relevant information
    for backtest run, such as the strategy, portfolio,
    broker and data handler. It should be possible to
    attach this information through the functions defined
    in the api.py and they should be unpacked for use in the
    __main__.py file.
    """
    strategy: Strategy