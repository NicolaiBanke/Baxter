from event.order import OrderEvent
from .execution_handler import ExecutionHandler
from queue import Queue
from event.event import EventType
from event.fill import FillEvent
import datetime
from typing import cast, Literal


class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self, events: Queue) -> None:
        """
        Docstring for __init__

        :param self: SimulatedExecutionHandler instance
        :param events: events queue
        :type events: Queue
        """

        self.events = events

    def execute_order(self, event: OrderEvent) -> None:
        if event.type == EventType.ORDER:
            fill_event = FillEvent(
                direction=cast(Literal["BUY", "SELL"], event.direction),
                exchange="ARCA",
                fill_cost=None,
                quantity=event.quantity,
                symbol=event.symbol,
                time_index=datetime.datetime.now(datetime.timezone.utc)
            )

            self.events.put(fill_event)
