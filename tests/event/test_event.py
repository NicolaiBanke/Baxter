import pytest
from evbax.event.event import Event


def test_event_instantiation():
    with pytest.raises(TypeError):
        Event(), "Event object should not be instantiable"
