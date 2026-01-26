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
from baxter.execution.simulated import SimulatedExecutionHandler
from baxter.backtest import Backtest
import logging
import quantstats as qs
import sys

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stdoutHandler = logging.StreamHandler(stream=sys.stdout)
stdoutHandler.setLevel(logging.DEBUG)

errHandler = logging.FileHandler("error.log")
errHandler.setLevel(logging.ERROR)

fmt = logging.Formatter(
    "{asctime} - {levelname}:{name}:{message}", style="{", datefmt="%Y-%m-%d %H:%M")

stdoutHandler.setFormatter(fmt)
errHandler.setFormatter(fmt)

logger.addHandler(stdoutHandler)
logger.addHandler(errHandler)

data_path = "/home/n1c0/Dropbox/Quant/Projects/baxter/tests"
symbols = ["SPY", "QQQ"]

events: Queue[Event] = Queue()

bars: DataHandler = HistoricHDF5DataHandler(
    events, data_path + "/test_hdf5data.h5", symbols)

# It should be possible to define a strategy in a Jupyter notebook or separate file, and pass it here
strategy: Strategy = Backtest.strategy if Backtest.strategy is not None else BuyAndHoldStrategy(bars=bars, events=events)

pf = NaivePortfolio(events=events, bars=bars)
broker = SimulatedExecutionHandler(events=events)


# the loop representing market events

def main():
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
                    logger.error(f"Event is {None}: {event}")
                    continue