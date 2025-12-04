import pytest
from evbax.event.event import Event


def test_event_instantiation():
    e = Event()
    with pytest.raises(AttributeError):
        assert e.type, "Event object should not have a type"
