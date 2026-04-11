from baxter.event.order import OrderEvent
from .execution_handler import ExecutionHandler
from queue import Queue
from baxter.event import Event, EventType
from baxter.event.fill import FillEvent
import datetime
import pandas as pd


class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self, events: Queue[Event]) -> None:
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
                direction=event.direction,
                exchange="ARCA",
                fill_cost=None,
                quantity=event.quantity,
                symbol=event.symbol,
                time_index=pd.Timestamp.now(datetime.timezone.utc),
            )

            self.events.put(fill_event)
