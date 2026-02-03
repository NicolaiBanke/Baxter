from ..event import MarketEvent, Event, EventType, SignalEvent, SignalType
from ..strategy import Strategy
from typing import Callable
from ..event import Event
from ..data import DataHandler, BarType
from queue import Queue

type InitStrategy = Callable[[DataHandler, Queue[Event]], Strategy]
type CalcSignal = Callable[[list[BarType]], None | SignalType]

def strategy_factory(_calculate_signals: CalcSignal, windows: dict[str, int]) -> InitStrategy:
    class GenericStrategy(Strategy):
        def __init__(self, bars: DataHandler, events: Queue[Event]) -> None:
            self.bars = bars
            self.events = events

            self.symbol_list = self.bars.symbol_list

        def calculate_signals(self, event: MarketEvent) -> None:
            if event.type == EventType.MKT:
                # go through each ticker and get the N=1 latest bars
                for ticker in self.symbol_list:
                    bars = self.bars.get_latest_bars(ticker, N=windows[ticker])
                    if bars is not None and bars != []:
                        signal_type = _calculate_signals(bars)
                        if signal_type:
                            signal = SignalEvent(
                                bars[-1][0], bars[-1][1], signal_type)
                            # put the signal in the events queue
                            self.events.put(signal)

    return GenericStrategy
