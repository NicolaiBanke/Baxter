from abc import ABC, abstractmethod
from ..event.signal import SignalEvent
from ..event.fill import FillEvent


class Portfolio(ABC):
    """
    Docstring for Portfolio

    Abstrat base class for the Portfolio objects. A derived portfolio
    class must implement methods to handle received SignalEvent and
    FillEvent.
    """

    @abstractmethod
    def update_signal(self, event: SignalEvent):
        raise NotImplementedError("Should implement .update_signal")

    @abstractmethod
    def update_fill(self, event: FillEvent):
        raise NotImplementedError("Shoul implement .update_fill")
