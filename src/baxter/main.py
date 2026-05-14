from baxter.backtest import run_algorithm
from pandas import Timestamp, HDFStore
from baxter.strategy.mean_reversion import MeanReversionStrategy


def main() -> None:
    # raise NotImplementedError("Should run the algorithm")
    results = run_algorithm(
        symbols=["SPY"],
        start_date=Timestamp(year=1999, month=3, day=10),
        end_date=Timestamp(year=2024, month=5, day=17),
        strategy_class=MeanReversionStrategy,
    )
    with HDFStore("/home/n1c0/.baxter/results/results.h5") as store:
        store.put("MeanReversionStrategy", results.equity_curve)
