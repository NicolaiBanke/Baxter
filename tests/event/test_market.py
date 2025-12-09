from baxter.event.market import MarketEvent
from baxter.event.event import EventType


def test_has_type_mkt():
    me = MarketEvent()
    assert me.type == EventType.MKT
