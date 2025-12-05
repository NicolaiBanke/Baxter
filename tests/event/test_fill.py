from evbax.event.fill import FillEvent
from evbax.types.event_type import EventType


def test_has_type_fill(fill_args):
    fe = FillEvent(*fill_args)
    assert fe.type == EventType.FILL
