from typing import Iterable, Type
from baxter.data import DataHandler, HistoricHDF5DataHandler
from queue import Queue
from baxter.event import Event
from baxter.strategy import Strategy
from baxter.portfolio import Portfolio, NaivePortfolio
from baxter.execution import ExecutionHandler, SimulatedExecutionHandler
from pathlib import Path
import os
import pandas as pd

try:
    baxter_root = os.environ["BAXTER_ROOT"]
except KeyError:
    print("Please ensure a BAXTER_ROOT environment variable is defined and accessible")
    exit()

DATA_PATH = Path(baxter_root, "data")


type InitAlgo = tuple[Queue[Event], DataHandler, Strategy, Portfolio, ExecutionHandler]


def initialize_algorithm(
    symbols: Iterable[str],
    strategy_class: Type[Strategy],
    start_date: pd.Timestamp,
    end_date: pd.Timestamp = pd.Timestamp.now(),
) -> InitAlgo:

    events: Queue[Event] = Queue()
    # for now, use HistoricHDF5DataHandler as default data handler
    bars: DataHandler = HistoricHDF5DataHandler(events, DATA_PATH / "data.h5", symbols)

    # portfolio and execution handler can also be defaults for now
    pf: Portfolio = NaivePortfolio(
        events=events, bars=bars, start_date=start_date, end_date=end_date
    )
    broker: ExecutionHandler = SimulatedExecutionHandler(events=events)

    strategy: Strategy = strategy_class(bars=bars, events=events)

    return events, bars, strategy, pf, broker
