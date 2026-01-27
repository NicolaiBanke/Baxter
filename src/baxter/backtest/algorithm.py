from queue import Queue, Empty
from baxter.event.event import Event
from baxter.event.signal import SignalEvent
from baxter.event.market import MarketEvent
from baxter.event.order import OrderEvent
from baxter.event.fill import FillEvent
from baxter.data.data_handler import DataHandler
from baxter.data.historic_hdf5 import HistoricHDF5DataHandler
from baxter.strategy.buynhold import BuyAndHoldStrategy
from baxter.strategy.strategy import Strategy
from baxter.portfolio.naive_portfolio import NaivePortfolio
from baxter.portfolio.portfolio import Portfolio
from baxter.execution.execution_handler import ExecutionHandler
from baxter.execution.simulated import SimulatedExecutionHandler
from baxter.backtest import setup_algorithm, analyze
from typing import Callable


symbols: list[str] = ["SPY", "QQQ"]


# It should be possible to define a strategy in a Jupyter notebook or separate file, and pass it here


pf: Portfolio = NaivePortfolio(events=events, bars=bars)
broker: ExecutionHandler = SimulatedExecutionHandler(events=events)


def run_algorithm(setup_algorithm = setup_algorithm, analyze: Callable = analyze):
    bars, strategy = setup_algorithm(symbols=symbols)
    
    while bars.continue_backtest:
        bars.update_bars()

    # handle the incoming events one by one
    while True:
        try:
            event = events.get(False)
        except Empty:
            break
        else:
            if event is not None:
                if isinstance(event, MarketEvent):
                    strategy.calculate_signals(event)
                    pf.update_timeindex(event)
                elif isinstance(event, SignalEvent):
                    pf.update_signal(event)
                elif isinstance(event, OrderEvent):
                    broker.execute_order(event)
                elif isinstance(event, FillEvent):
                    pf.update_fill(event)
                else:
                    continue
            else:
                continue

    analyze()
