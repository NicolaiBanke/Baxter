from enum import Enum


class Event(object):
    """
    Docstring for Event

    The base class for the Event objects. It serves only as an interface
    for derived classes and holds no functionality itself.
    """
    pass


class EventType(Enum):
    """
    Docstring for EventType

    The different types of events.
    """

    MKT = "Market"
    ORDER = "Order"
    FILL = "Fill"
    SIGNAL = "Signal"
