from queue import Queue, Empty
from event.event import Event
from event.market import MarketEvent
from data.data_handler import DataHandler
from data.historic_hdf5 import HistoricHDF5DataHandler
from strategy.buynhold import BuyAndHoldStrategy
from strategy.strategy import Strategy
from portfolio.naive_portfolio import NaivePortfolio
from execution.simulated import SimulatedExecutionHandler

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
                    if isinstance(event, MarketEvent): #event.type == EventType.MKT:
                        strategy.calculate_signals(event)
                        pf.update_timeindex(event)
                        bars.continue_backtest = False


if __name__ == "__main__":
    main()
