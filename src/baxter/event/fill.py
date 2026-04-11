from baxter.event.event import Event
from baxter.event.event import EventType
from typing import Literal
import pandas as pd


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
    - fill_cost: the cost of the fill
    - time_index: the timestamp of the fill
    """

    @property
    def type(self):
        return EventType.FILL

    def __init__(
        self,
        symbol: str,
        quantity: int,
        direction: Literal["BUY", "SELL"],
        exchange: str,
        fill_cost: float | None,
        time_index: pd.Timestamp,
    ):
        self.symbol: str = symbol
        self.quantity: int = quantity
        self.direction: Literal["BUY", "SELL"] = direction
        self.exchange: str = exchange
        self.fill_cost: int | float | None = fill_cost
        self.commission = 0.0  # should be able to set
        self.time_index: pd.Timestamp = time_index

    def __repr__(self) -> str:
        return f"{self.direction} {self.quantity} shares of {self.symbol} on {self.exchange} at {self.time_index}"

    def _calculate_commission(self):
        raise NotImplementedError("Should calculate the relevant commission.")
