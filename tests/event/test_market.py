from event.market import MarketEvent
from event.event import EventType


def test_has_type_mkt():
    me = MarketEvent()
    assert me.type == EventType.MKT
