import pytest
from queue import Queue
from baxter.event import MarketEvent, Event, OrderEvent
from baxter.event.order import OrderType
from baxter.execution.saxo import SaxoExecutionHandler
from baxter.data import HistoricHDF5DataHandler
from pathlib import Path


@pytest.fixture(scope="module")
def events_queue() -> Queue[Event]:
    q: Queue[Event] = Queue()
    q.put(MarketEvent())
    return q


@pytest.fixture(scope="module")
def symbol_list() -> list[str]:
    return ["NOVOb", "SPY"]


@pytest.fixture(scope="module")
def mkt_order(symbol_list) -> OrderEvent:
    return OrderEvent(
        direction="BUY", order_type=OrderType["MKT"], quantity=10, symbol=symbol_list[0]
    )


@pytest.fixture(scope="module")
def saxo_execution_handler(events_queue) -> SaxoExecutionHandler:
    return SaxoExecutionHandler(events=events_queue)


@pytest.fixture(scope="module", params=["data"])
def historic_hdf5_data_handler(
    symbol_list, events_queue, request, monkeypatch: pytest.MonkeyPatch
) -> HistoricHDF5DataHandler:
    return HistoricHDF5DataHandler(
        events=events_queue, symbol_list=symbol_list, hdf5_dir=Path("")
    )
