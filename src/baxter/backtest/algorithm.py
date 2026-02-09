from queue import Empty
from ..event import SignalEvent, MarketEvent, OrderEvent, FillEvent
from ..backtest.initialization import initialize_algorithm, CalcSignal
from ..portfolio import Portfolio


def run_algorithm(symbols: list[str],
                  calculate_signals: CalcSignal, N: int) -> Portfolio:
    events, bars, strategy, pf, broker = initialize_algorithm(
        symbols=symbols, calculate_signals=calculate_signals, N=N)

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
