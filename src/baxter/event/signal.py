from event import Event, EventType
from datetime import datetime
from enum import Enum


class SignalType(Enum):
    """
    Docstring for SignalType

    The two different signal types are 'LONG' and 'SHORT'.
    """

    LONG = "Long"
    SHORT = "Short"


class SignalEvent(Event):
    @property
    def type(self):
        return EventType.SIGNAL

    def __init__(self, symbol: str, datetime: datetime, signal_type: SignalType) -> None:
        """
        Docstring for __init__
        
        :param self: Description
        :param symbol: Description
        :type symbol: str
        :param datetime: Description
        :type datetime: datetime
        :param signal_type: Description
        :type signal_type: SignalType
        """
        
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
