from portfolio.naive_portfolio import NaivePortfolio
from queue import Queue
from event.event import Event
from data.data_handler import DataHandler
from pytest_mock import MockerFixture
from queue import Queue
from event.market import MarketEvent
from data.data_handler import BarType
from typing import List

# .update_timeindex should only append current holdings and positions to corresponding properties


def test_update_timeindex(data_handler: DataHandler, events_queue: Queue[Event], mocker: MockerFixture, bar: BarType, symbol_list: List[str]):
    # mock bars by mocking DataHandler fixture's method
    npf = NaivePortfolio(data_handler, events_queue)
    mocker.patch("data.data_handler.DataHandler.get_latest_bars", bar)
    mocker.patch("data.data_handler.DataHandler.symbol_list", symbol_list)
    npf.update_timeindex(MarketEvent())
    assert npf.all_positions[::-1].pop() == {
        
    }
    assert npf.all_holdings[::-1].pop() == bar


def test_update_fill():
    pass


def test_update_signal():
    pass
