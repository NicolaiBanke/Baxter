from queue import Empty
from baxter.event.signal import SignalEvent
from baxter.event.market import MarketEvent
from baxter.event.order import OrderEvent
from baxter.event.fill import FillEvent
from baxter.backtest.setup import initialize_algorithm, InitAlgo
from baxter.portfolio import Portfolio
from typing import Callable


symbols: list[str] = ["SPY", "QQQ"]


# It should be possible to define a strategy in a Jupyter notebook or separate file, and pass it here


def run_algorithm(initialize_algorithm: Callable[[], InitAlgo] = initialize_algorithm) -> Portfolio:
    events, bars, strategy, pf, broker = initialize_algorithm()

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
    pf.create_equity_curve_dataframe()
    return pf
