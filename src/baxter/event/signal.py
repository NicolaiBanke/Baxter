from .event import Event, EventType
from enum import Enum
import pandas as pd


class SignalType(Enum):
    """
    Docstring for SignalType

    The two different signal types are 'LONG' and 'SHORT'.
    """

    LONG = "Long"
    SHORT = "Short"
    EXIT = "Exit"


class SignalEvent(Event):
    @property
    def type(self):
        return EventType.SIGNAL

    def __init__(
        self, symbol: str, datetime: pd.Timestamp, signal_type: SignalType
    ) -> None:
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

        self.symbol: str = symbol
        self.datetime: pd.Timestamp = datetime
        self.signal_type: SignalType = signal_type
