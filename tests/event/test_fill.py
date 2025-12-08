from baxter.event.fill import FillEvent
from baxter.event.event import EventType


def test_has_type_fill(fill_args):
    fe = FillEvent(*fill_args)
    assert fe.type == EventType.FILL
