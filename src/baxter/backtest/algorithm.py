from baxter.strategy import Strategy
from typing import Iterable, Type
from queue import Empty
from ..event import SignalEvent, MarketEvent, OrderEvent, FillEvent, Event
from ..backtest.initialization import initialize_algorithm
from ..portfolio import Portfolio
import pandas as pd


def run_algorithm(
    symbols: Iterable[str],
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    strategy_class: Type[Strategy],
) -> Portfolio:
    events, bars, strategy, pf, broker = initialize_algorithm(
        symbols=symbols,
        strategy_class=strategy_class,
        start_date=start_date,
        end_date=end_date,
    )

    while bars.continue_backtest:
        bars.update_bars()

        # handle the incoming events one by one
        while True:
            try:
                event: Event = events.get(False)
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
