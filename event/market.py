from event.event import Event, EventType


class MarketEvent(Event):
    """
    Docstring for MarketEvent

    The event representing a new heartbeat
    of the market. It should have no functionality
    (so far), and should only be identified with its type. 
    """

    @property
    def type(self):
        return EventType.MKT
