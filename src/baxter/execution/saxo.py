from baxter.event.order import OrderEvent
from .execution_handler import ExecutionHandler
from queue import Queue
from baxter.event import Event, EventType
from baxter.event.fill import FillEvent
import datetime
from typing import cast, Literal
from saxo_openapi import OpenAPIError, API
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.session import account_info
import os

# there aren't separate execution handlers for sim and live saxo accounts, as these will be distinquished by the API token, I think


class SaxoExecutionHandler(ExecutionHandler):
    def __init__(self, events: Queue[Event]) -> None:

        self.events = events

        self._create_saxo_connection()

    def _create_saxo_connection(self):
        saxo_token = os.environ.get('SAXO_API')

        try:
            self.client = API(access_token=saxo_token)
            self.account = account_info(self.client)
        except OpenAPIError:
            print("Invalid API key")

    def _create_saxo_order(self):
        raise NotImplementedError

    # should possibly be public method
    def _create_fill(self, event: FillEvent):
        # should put fill event on queue when .execute_order gets confirmation that the order went through
        fill_event = FillEvent(
            direction=cast(Literal["BUY", "SELL"], event.direction),
            exchange="ARCA",
            fill_cost=None,
            quantity=event.quantity,
            symbol=event.symbol,
            time_index=datetime.datetime.now(datetime.timezone.utc)
        )

        self.events.put(fill_event)
        raise NotImplementedError

    def execute_order(self, event: OrderEvent) -> None:
        if event.type == EventType.ORDER:
            pass
