from typing import Iterable
from baxter.data import DataHandler, HistoricHDF5DataHandler
from queue import Queue
from baxter.event import Event
from baxter.strategy import Strategy
from baxter.portfolio import Portfolio, NaivePortfolio
from baxter.execution import ExecutionHandler, SimulatedExecutionHandler
from datetime import datetime
from pathlib import Path
from ..factories import strategy_factory, CalcSignal
import os

try:
    baxter_root = os.environ["BAXTER_ROOT"]
except KeyError:
    print("Please ensure a BAXTER_ROOT environment variable is defined and accessible")
    exit()

DATA_PATH = Path(baxter_root, "data")


type InitAlgo = tuple[Queue[Event], DataHandler, Strategy, Portfolio, ExecutionHandler]


def initialize_algorithm(
    symbols: Iterable[str], calculate_signals: CalcSignal, N: int
) -> InitAlgo:

    events: Queue[Event] = Queue()
    # for now, use HistoricHDF5DataHandler as default data handler
    bars: DataHandler = HistoricHDF5DataHandler(events, DATA_PATH / "data.h5", symbols)

    # portfolio and execution handler can also be defaults for now
    pf: Portfolio = NaivePortfolio(
        events=events, bars=bars, start_date=datetime(1999, 3, 9)
    )
    broker: ExecutionHandler = SimulatedExecutionHandler(events=events)

    strategy = strategy_factory(N)(calculate_signals)(bars, events)

    return events, bars, strategy, pf, broker
