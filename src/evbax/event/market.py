from evbax.event.event import Event


class MarketEvent(Event):
    """
    Docstring for MarketEvent

    The event representing a new heartbeat
    of the market. It should have no functionality
    (so far), and should only be identified with its type. 
    """

    def __init__(self):
        self.type = 'MKT'
