from abc import abstractmethod, ABC
from typing import List, Tuple
from datetime import datetime
from queue import Queue

type BarType = Tuple[str, datetime, *Tuple[float, ...]]


class DataHandler(ABC):
    """
    Docstring for DataHandler

    Abstract base class for data handlers.
    Every data handler should implement methods to
    send off data into the event loop.
    """

    @property
    @abstractmethod
    def symbol_list(self) -> List[str]: ...

    @property
    @abstractmethod
    def continue_backtest(self) -> bool: ...

    @continue_backtest.setter
    @abstractmethod
    def continue_backtest(self, new_setting: bool) -> None: ...

    @abstractmethod
    def get_latest_bars(self, symbol, N=1) -> List[BarType] | None: ...

    @abstractmethod
    def update_bars(self) -> None: ...
