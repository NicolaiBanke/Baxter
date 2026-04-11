from ..event import MarketEvent, Event, EventType, SignalEvent, SignalType
from ..strategy import Strategy
from typing import Callable
from ..data import DataHandler, BarType
from queue import Queue

type InitStrategy = Callable[[DataHandler, Queue[Event]], Strategy]
type CalcSignal = Callable[[list[BarType]], None | SignalType]


def strategy_factory(N: int) -> Callable[[CalcSignal], InitStrategy]:
    def wrapper(_calculate_signals: CalcSignal) -> InitStrategy:
        class GenericStrategy(Strategy):
            def __init__(self, bars: DataHandler, events: Queue[Event]) -> None:
                self.bars: DataHandler = bars
                self.events: Queue[Event] = events

                self.symbol_list: list[str] = self.bars.symbol_list

            def calculate_signals(self, event: MarketEvent) -> None:
                if event.type == EventType.MKT:
                    # go through each ticker and get the N latest bars
                    for ticker in self.symbol_list:
                        bars: list[BarType] = self.bars.get_latest_bars(ticker, N=N)
                        if bars is not None and len(bars) >= N:  # != []:
                            signal_type: None | SignalType = _calculate_signals(bars)
                            if signal_type is not None:
                                signal = SignalEvent(
                                    bars[-1][0], bars[-1][1], signal_type
                                )

                                # put the signal in the events queue
                                self.events.put(signal)

        return GenericStrategy

    return wrapper
