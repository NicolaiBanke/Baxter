from evbax.event.event import Event
from evbax.types.event_type import EventType
from datetime import datetime


class FillEvent(Event):
    """
    Docstring for FillEvent

    The Event object for the event of filling an order.
    It should have several attributes, of which all but
    'type' are passed to the initializer.

    Attributes:
    - type: the type of the order
    - symbol: ticker symbol of the order being filled
    - quantity: the amount of assets in the order
    - direction: 'BUY' or 'SELL'
    - exchange: the exchange on which the order is being filled
    - fill_cost: the cost of the fill? <-- brush up
    - time_index: the timestamp of the fill?  <-- brush up
    """

    def __init__(self, symbol: str, quantity: int, direction: str, exchange: str, fill_cost: float, time_index: datetime):
        self.type = EventType.FILL
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.exchange = exchange
        self.fill_cost = fill_cost
        self.time_index = time_index
