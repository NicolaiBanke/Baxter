from enum import Enum


class OrderType(Enum):
    """
    Docstring for OrderType

    The different types of orders.

    MKT = 'Market order'
    LIM = 'Limit order'
    """
    MKT = "Market order"
    LIM = "Limit order"
