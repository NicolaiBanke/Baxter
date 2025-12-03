from abc import abstractmethod, ABC


class DataHandler(ABC):
    """
    Docstring for DataHandler

    Abstract base class for data handlers.
    Every data handler should implement methods to
    send off data into the event loop.
    """


    @abstractmethod
    def get_latest_bars(self, N=1): ...#forgot 'symbol' parameter

    @abstractmethod
    def update_bars(self): ...
