from evbax.event.event import Event
from evbax.types.order_type import OrderType
from evbax.types.event_type import EventType


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

    def __init__(self, symbol: str, quantity: int, direction: str, order_type: OrderType):
        self.type = EventType.ORDER
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.order_type = order_type
