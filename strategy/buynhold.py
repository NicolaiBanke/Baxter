from ..event.event import EventType
from ..event.market import MarketEvent
from ..event.signal import SignalEvent, SignalType
from ..strategy.strategy import Strategy
from ..data.data_handler import DataHandler
from queue import Queue


class BuyAndHoldStrategy(Strategy):
    def __init__(self, bars: DataHandler, events: Queue) -> None:
        """
        Docstring for __init__

        :param self: The Strategy instance.
        :param bars: The DataHandler object providing the bars.
        :type bars: DataHandler
        :param events: The events queue.
        :type events: Queue
        """
        self.bars = bars
        self.events = events

        # the list of ticker symbols
        self.symbol_list = bars.symbol_list

        # a dict indicating whether the symbols have been bought
        self.bought: dict[str, bool] = self._calculate_initial_bought()

    def _calculate_initial_bought(self) -> dict[str, bool]:
        bought = {}
        for symbol in self.symbol_list:
            self.bought[symbol] = False
        return bought

    def calculate_signals(self, event: MarketEvent) -> None:
        if event.type == EventType.MKT:
            # go through each ticker and get the N=1 latest bars
            for ticker in self.symbol_list:
                bars = self.bars.get_latest_bars(ticker)
                if bars is not None and bars != []:
                    # buy if not bought already
                    if not self.bought[ticker]:
                        # generate a SignalEvent with signature (symbol, datetime, type = LONG, SHORT, EXIT)
                        signal = SignalEvent(
                            bars[0][0], bars[0][1], SignalType.LONG)
                        # put the signal in the events queue
                        self.events.put(signal)
                        # note the ticker as bought - maybe a method could set this when a FillEvent is received confirming the trade?
                        self.bought[ticker] = True
