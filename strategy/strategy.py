from abc import ABC, abstractmethod
from event.market import MarketEvent


class Strategy(ABC):
    """
    Docstring for Strategy

    Abstract base class for any strategy programmed to be tested by
    the backtester. The interface enforces the implementation of a
    method to calculate the signals, based on the data provided by
    the DataHandler subclassed instance.
    """

    @abstractmethod
    def calculate_signals(self, event: MarketEvent):
        """
        Docstring for calculate_signals

        :param self: Description
        :param event: Description
        :type event: MarketEvent

        Calculates the Signal Events which are sent and acted on
        by the Portfolio object.
        """
        raise NotImplementedError("Should implement .calculate_signals")
