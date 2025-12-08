from baxter.event.order import OrderEvent
from baxter.event.event import EventType


def test_has_type_order(order_args):
    oe = OrderEvent(*order_args)
    assert oe.type == EventType.ORDER
