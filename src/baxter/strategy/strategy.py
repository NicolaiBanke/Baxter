from baxter.event import Event
from queue import Queue
from baxter.data import DataHandler
from abc import ABC, abstractmethod
from baxter.event.market import MarketEvent


class Strategy(ABC):
    """
    Docstring for Strategy

    Abstract base class for any strategy programmed to be tested by
    the backtester. The interface enforces the implementation of a
    method to calculate the signals, based on the data provided by
    the DataHandler subclassed instance.
    """
    
    @abstractmethod
    def __init__(self, bars: DataHandler, events: Queue[Event]):
        raise NotImplementedError("Strategy must be initialized with a DataHandler and Event Queue")

    @abstractmethod
    def calculate_signals(self, event: MarketEvent) -> None:
        """
        Docstring for calculate_signals

        :param self: Strategy instance.
        :param event: market event which triggers the calculations.
        :type event: MarketEvent

        Calculates the Signal Events which are sent and acted on
        by the Portfolio object.
        """
        raise NotImplementedError("Should implement .calculate_signals")
