from baxter.data import DataHandler, HistoricHDF5DataHandler
from typing import Callable
from queue import Queue
from baxter.event import Event
from baxter.strategy import Strategy, BuyAndHoldStrategy

DATA_PATH: str = "/home/n1c0/Dropbox/Quant/Projects/baxter/tests"


def setup_algorithm(
        symbols: list[str] = ['SPY'],
        data_handler: Callable[[Queue[Event], str, list[str]],
                               DataHandler] = HistoricHDF5DataHandler,
        strategy_init: Callable[[DataHandler, Queue[Event]], Strategy] = BuyAndHoldStrategy) -> tuple[DataHandler, Strategy]:
    events: Queue[Event] = Queue()
    bars: DataHandler = data_handler(
        events, DATA_PATH + "/test_hdf5data.h5", symbols)
    strategy: Strategy = strategy_init(bars, events)

    return bars, strategy
