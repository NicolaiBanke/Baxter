from enum import Enum
from event.event import Event, EventType
from typing import Literal


class OrderType(Enum):
    """
    Docstring for OrderType

    The different types of orders.

    MKT = 'Market order'
    LIM = 'Limit order'
    """
    MKT = "Market order"
    LIM = "Limit order"


class OrderEvent(Event):
    """
    Docstring for OrderEvent

    The Event object which models the ordering of a trade.
    It is sent by the Strategy object and received by the
    ExecutionHandler object to fill the order.

    Attributes:
    - type: the type of the order
    - symbol: ticker symbol of the order being filled
    - quantity: the amount of assets in the order
    - direction: 'BUY' or 'SELL'
    - order_type: 'MKT' (market order) or 'LIM' (limit order)
    """

    @property
    def type(self):
        return EventType.ORDER

    def __init__(self, symbol: str, quantity: int, direction: Literal["BUY", "SELL"], order_type: OrderType):
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.order_type = order_type
