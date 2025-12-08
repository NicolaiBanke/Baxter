from abc import abstractmethod, ABC
from typing import List


class DataHandler(ABC):
    """
    Docstring for DataHandler

    Abstract base class for data handlers.
    Every data handler should implement methods to
    send off data into the event loop.
    """

    @abstractmethod
    def get_latest_bars(self, symbol, N=1) -> List | None: ...

    @abstractmethod
    def update_bars(self) -> None: ...
