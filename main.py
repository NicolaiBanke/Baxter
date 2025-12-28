from queue import Queue, Empty
from event.event import Event
from event.signal import SignalEvent
from event.market import MarketEvent
from event.order import OrderEvent
from event.fill import FillEvent
from data.data_handler import DataHandler
from data.historic_hdf5 import HistoricHDF5DataHandler
from strategy.buynhold import BuyAndHoldStrategy
from strategy.strategy import Strategy
from portfolio.naive_portfolio import NaivePortfolio
from execution.simulated import SimulatedExecutionHandler
import logging
import time

# logging config
logging.basicConfig(level=logging.INFO,
                    format="{asctime} - {levelname}:{name}:{message}", style="{", datefmt="%Y-%m-%d %H:%M")

data_path = "/home/n1c0/Dropbox/Quant/Projects/baxter/tests"
symbols = ["SPY", "QQQ"]

events: Queue[Event] = Queue()

bars: DataHandler = HistoricHDF5DataHandler(
    events, data_path + "/test_hdf5data.h5", symbols)
strategy: Strategy = BuyAndHoldStrategy(bars=bars, events=events)
pf = NaivePortfolio(events=events, bars=bars)
broker = SimulatedExecutionHandler(events=events)


# the loop representing market events

def main():
    logging.info("Event loop starts")
    while bars.continue_backtest:
        bars.update_bars()

        # handle the incoming events one by one
        while True:
            try:
                event = events.get(False)
                logging.info(f"Event: {event.type}")
            except Empty:
                logging.info("Event queue is empty.")
                break
            else:
                if event is not None:
                    # if event.type == EventType.MKT:
                    if isinstance(event, MarketEvent):
                        strategy.calculate_signals(event)
                        pf.update_timeindex(event)
                        #bars.continue_backtest = False
                    elif isinstance(event, SignalEvent):
                        pf.update_signal(event)
                    elif isinstance(event, OrderEvent):
                        broker.execute_order(event)
                    elif isinstance(event, FillEvent):
                        pf.update_fill(event)
                    else:
                        continue
                else:
                    logging.error("Event is None.")
        time.sleep(.1)


if __name__ == "__main__":
    main()
