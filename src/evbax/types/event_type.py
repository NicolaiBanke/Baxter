from enum import Enum


class EventType(Enum):
    """
    Docstring for EventType

    The different types of events.
    """

    MKT = "Market"
    ORDER = "Order"
    FILL = "Fill"
    SIGNAL = "Signal"
