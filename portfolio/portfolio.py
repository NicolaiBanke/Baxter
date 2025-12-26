from abc import ABC, abstractmethod
from event.signal import SignalEvent
from event.fill import FillEvent


class Portfolio(ABC):
    """
    Docstring for Portfolio

    Abstrat base class for the Portfolio objects. A derived portfolio
    class must implement methods to handle received SignalEvent and
    FillEvent.
    """

    @abstractmethod
    def update_signal(self, signal_event: SignalEvent) -> None:
        raise NotImplementedError("Should implement .update_signal")

    @abstractmethod
    def update_fill(self, fill_event: FillEvent) -> None:
        raise NotImplementedError("Shoul implement .update_fill")
