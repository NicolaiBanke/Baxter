from baxter.event.order import OrderEvent
from .execution_handler import ExecutionHandler
from queue import Queue
from baxter.event.event import EventType
from baxter.event.fill import FillEvent
import datetime
from typing import cast, Literal
import logging
import sys

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stdoutHandler = logging.StreamHandler(stream=sys.stdout)
stdoutHandler.setLevel(logging.DEBUG)

errHandler = logging.FileHandler("error.log")
errHandler.setLevel(logging.ERROR)

fmt = logging.Formatter(
    "{asctime} - {levelname}:{name}:{message}", style="{", datefmt="%Y-%m-%d %H:%M")

stdoutHandler.setFormatter(fmt)
errHandler.setFormatter(fmt)

logger.addHandler(stdoutHandler)
logger.addHandler(errHandler)

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
            logger.info(f"Sent fill event: {fill_event}")
