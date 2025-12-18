import pytest
from datetime import datetime
from queue import Queue
from baxter.event.market import MarketEvent
from typing import Tuple, List
from baxter.data.data_handler import DataHandler


# generic Queue object with a single MarketEvent in it
@pytest.fixture(scope="module")
def events_queue() -> Queue:
    q = Queue()
    q.put(MarketEvent())
    return q

# generic symbol list longer than 1


@pytest.fixture(scope="module")
def symbol_list():
    return ["SPY", "QQQ"]

# arguments for a generic FillEvent object


@pytest.fixture(scope="module")
def fill_args():
    # symbol, quantity, direction, exchange, fill_cost, time_index
    return ["symbol", 1, "BUY", "exchange", 1.0, datetime.now()]


# arguments for a generic OrderEvent object
@pytest.fixture
def order_args():
    # symbol, quantity, direction, order_type
    return ["symbol", 1, "BUY", "MKT"]


# arguments for a generic DataHandler subobject
@pytest.fixture(scope="module")
def data_handler_args(events_queue) -> Tuple[Queue, str, List[str]]:
    # events, hdf5_dir, symbol_list
    return (events_queue, "/home/n1c0/Dropbox/Quant/Projects/baxter/tests/test_hdf5data.h5", ["SPY", "QQQ"])