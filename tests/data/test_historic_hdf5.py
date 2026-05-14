from typing import Iterator
from pytest import MonkeyPatch
from pathlib import Path
from queue import Queue
from baxter.event import Event
from baxter.data.historic_hdf5 import HistoricHDF5DataHandler
from hypothesis import given
from data_validation import PriceDataSchema
from pandera.typing import DataFrame
from baxter.data import BarType
import baxter.data


@given(data=PriceDataSchema.strategy(size=10))
def test_symbol_data(
    data: DataFrame[PriceDataSchema], events_queue: Queue[Event], symbol_list: list[str]
):
    with MonkeyPatch().context() as monkeypatch:
        monkeypatch.setattr(
            target=baxter.data.historic_hdf5,
            name="get_validated_data",
            value=lambda hdf5_dir, ticker: data,
        )
        historic_hdf5_data_handler = HistoricHDF5DataHandler(
            events=events_queue, symbol_list=symbol_list, hdf5_dir=Path("")
        )
        for symbol in symbol_list:
            assert isinstance(
                historic_hdf5_data_handler.symbol_data[symbol], Iterator
            ), "dict value must be an iterator"


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
        for _ in range(2 * N):
            historic_hdf5_data_handler.update_bars()
        bars: list[BarType] = historic_hdf5_data_handler.get_latest_bars(
            symbol="SPY", N=N
        )
        assert len(bars) == N, f"get_latest_bars should get {N} bars"


@given(data=PriceDataSchema.strategy(size=10))
def test_update_bars(
    data: DataFrame[PriceDataSchema], events_queue: Queue[Event], symbol_list: list[str]
):
    with MonkeyPatch().context() as monkeypatch:
        monkeypatch.setattr(
            target=baxter.data.historic_hdf5,
            name="get_validated_data",
            value=lambda hdf5_dir, ticker: data,
        )
        historic_hdf5_data_handler = HistoricHDF5DataHandler(
            events=events_queue, symbol_list=symbol_list, hdf5_dir=Path("")
        )
        before = len(historic_hdf5_data_handler.latest_symbol_data[symbol_list[0]])
        historic_hdf5_data_handler.update_bars()
        after = len(historic_hdf5_data_handler.latest_symbol_data[symbol_list[0]])
        assert after == before + 1, (
            "update_bars should append a single bar to the latest_symbol_data property"
        )
