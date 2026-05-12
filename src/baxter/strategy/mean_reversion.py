from baxter.strategy import Strategy
from baxter.data import DataHandler
from baxter.event import Event, MarketEvent, EventType
from baxter.data.data_handler import BarType
from baxter.event.signal import SignalEvent, SignalType
from queue import Queue
import numpy as np


class MeanReversionStrategy(Strategy):
    def __init__(self, bars: DataHandler, events: Queue[Event]):
        self.bars: DataHandler = bars
        self.events: Queue[Event] = events

        # the list of ticker symbols
        self.symbol_list: list[str] = bars.symbol_list

    def calculate_signals(self, event: MarketEvent) -> None:
        if event.type == EventType.MKT:
            for ticker in self.symbol_list:
                bar: list[BarType] = self.bars.get_latest_bars(N=25, symbol=ticker)
                # indicators
                hml: float = np.mean(list(map(lambda x: x[3] - x[4], bar)))
                ibs: float = (bar[-1][5] - bar[-1][4]) / (bar[-1][3] - bar[-1][4])
                lband: float = max(map(lambda x: x[3], bar[-10:])) - 2.5 * hml

                if bar[-1][5] < lband and ibs < 0.3:
                    signal = SignalEvent(bar[0][0], bar[0][1], SignalType.LONG)
                    # put the signal in the events queue
                    self.events.put(signal)
                elif bar[-1][5] > bar[-2][5]:
                    signal = SignalEvent(bar[0][0], bar[0][1], SignalType.EXIT)
                    # put the signal in the events queue
                    self.events.put(signal)
                else:
                    pass
