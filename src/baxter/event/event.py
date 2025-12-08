from enum import Enum
from abc import ABC, abstractmethod
from typing import Literal


class Event(ABC):
    """
    Docstring for Event

    The base class for the Event objects. It serves only as an interface
    for derived classes and holds no functionality itself.
    """
    @property
    @abstractmethod
    def type(self) -> EventType: ...


class EventType(Enum):
    """
    Docstring for EventType

    The different types of events.
    """

    MKT = "Market"
    ORDER = "Order"
    FILL = "Fill"
    SIGNAL = "Signal"
