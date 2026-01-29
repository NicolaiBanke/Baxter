from baxter.data import DataHandler, HistoricHDF5DataHandler
from typing import Callable
from queue import Queue
from baxter.event import Event, MarketEvent
from baxter.strategy import Strategy, BuyAndHoldStrategy
from baxter.portfolio import Portfolio, NaivePortfolio
from baxter.execution import ExecutionHandler, SimulatedExecutionHandler
from datetime import datetime

# this should probably be an .env variable
DATA_PATH: str = "/home/n1c0/Dropbox/Quant/Projects/baxter/tests"

type InitStrat = Callable[[DataHandler, Queue[Event]], Strategy]
type InitAlgo = tuple[Queue[Event], DataHandler,
                      Strategy, Portfolio, ExecutionHandler]


def initialize_algorithm(
        # symbols could also be a global variable containing an entire universe of many symbols
        symbols: list[str] = ['SPY'],
        strategy: InitStrat = BuyAndHoldStrategy) -> InitAlgo:
    """
    Docstring for initialize_algorithm

    :param symbols: Ticker symbols to be traded
    :type symbols: list[str]
    :param strategy: Strategy class to test. Defaults to BuyAndHoldStrategy
    :type strategy: InitStrat
    :return: A tuple of events, data_handler, strategy, portfolio and execution_handler to use in the backtest
    :rtype: InitAlgo

    Default setup for a backtested algorithm
    """

    events: Queue[Event] = Queue()
    # for now, use HistoricHDF5DataHandler as default data handler
    bars: DataHandler = HistoricHDF5DataHandler(
        events, DATA_PATH + "/test_hdf5data.h5", symbols)

    # portfolio and execution handler can also be defaults for now
    pf: Portfolio = NaivePortfolio(
        events=events, bars=bars, start_date=datetime(1999, 3, 9))
    broker: ExecutionHandler = SimulatedExecutionHandler(events=events)

    return events, bars, strategy(bars, events), pf, broker


# factory method to generate a generic strategy by providing the definition for the .calculate_signals method
# use as a @decorator
def strategy_factory(compute: Callable[[Event], None]) -> Callable[[], InitStrat]:
    def wrapper() -> InitStrat:
        class GenericStrategy(Strategy):
            def __init__(self, bars, events) -> None:
                self.bars = bars
                self.events = events

            def calculate_signals(self, event: MarketEvent) -> None:
                return compute(event)

        return GenericStrategy

    return wrapper
