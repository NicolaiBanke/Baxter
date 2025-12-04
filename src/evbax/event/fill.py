from evbax.event.event import Event


class FillEvent(Event):
    """
    Docstring for FillEvent

    The Event object for the event of filling an order.
    It should have several attributes, of which all but
    'type' are passed to the initializer.

    Attributes:
    - type: the type of the order
    - symbol: ticker symbol of the order being filled
    - exchange: the exchange on which the order is being filled
    - fill_cost: the cost of the fill? <-- brush up
    - time_index: the timestamp of the fill?  <-- brush up
    - quantity: the amount of assets in the order
    - direction: 'BUY' or 'SELL'
    """

    def __init__(self, symbol, exchange, fill_cost, time_index, quantity, direction):
        self.type = 'FILL'
        self.symbol = symbol
        self.exchange = exchange
        self.fill_cost = fill_cost
        self.time_index = time_index
        self.quantity = quantity
        self.direction = direction
