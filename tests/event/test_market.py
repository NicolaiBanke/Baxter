import pytest
from evbax.event.market import MarketEvent


def test_has_type_mkt():
    me = MarketEvent()
    assert me.type == "MKT"
