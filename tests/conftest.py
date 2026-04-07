import pytest
from queue import Queue
from baxter.event import MarketEvent, Event, OrderEvent
from baxter.event.order import OrderType
from baxter.execution.saxo import SaxoExecutionHandler


@pytest.fixture(scope="module")
def events_queue() -> Queue[Event]:
    q: Queue[Event] = Queue()
    q.put(MarketEvent())
    return q


@pytest.fixture(scope="module")
def symbol_list() -> list[str]:
    return ["NOVOb"]


@pytest.fixture(scope="module")
def mkt_order(symbol_list) -> OrderEvent:
    return OrderEvent(
        direction="BUY", order_type=OrderType["MKT"], quantity=10, symbol=symbol_list[0]
    )


@pytest.fixture(scope="module")
def saxo_execution_handler(mkt_order) -> SaxoExecutionHandler:
    queue = Queue()
    queue.put(mkt_order)
    return SaxoExecutionHandler(events=queue)
