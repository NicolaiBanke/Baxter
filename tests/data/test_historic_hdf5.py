from pytest import MonkeyPatch
from pathlib import Path
from queue import Queue
from baxter.event import Event
from baxter.data.historic_hdf5 import HistoricHDF5DataHandler
from hypothesis import given
from data_validation import PriceDataSchema
from pandera.typing import DataFrame
import baxter.data


@given(data=PriceDataSchema.strategy(size=10))
def test_get_latest_bars(
    data: DataFrame[PriceDataSchema], events_queue: Queue[Event], symbol_list: list[str]
):
    with MonkeyPatch().context() as monkeypatch:
        N = 5
        monkeypatch.setattr(
            target=baxter.data.historic_hdf5,
            name="get_validated_data",
            value=lambda hdf5_dir, ticker: data,
        )
        historic_hdf5_data_handler = HistoricHDF5DataHandler(
            events=events_queue, symbol_list=symbol_list, hdf5_dir=Path("")
        )
        bars = historic_hdf5_data_handler.get_latest_bars(symbol="SPY", N=N)
        assert len(bars) == N
