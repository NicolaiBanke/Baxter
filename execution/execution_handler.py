from abc import ABC, abstractmethod
from event.order import OrderEvent


class ExecutionHandler(ABC):
    """
    Docstring for ExecutionHandler

    Base class interface for execution handlers. All handlers
    must implement a method to execute an order, and can be
    used to simulate the process of interacting with a brokerage.
    """
    @abstractmethod
    def execute_order(self, event: OrderEvent):
        """
        Docstring for execute_order

        :param self: ExecutionHandler instance
        :param event: the event to respond to, in this case an OrderEvent
        :type event: OrderEvent
        """
        raise NotImplementedError("Should implement .execute_order")
