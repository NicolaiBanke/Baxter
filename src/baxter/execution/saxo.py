from baxter.event.order import OrderEvent, OrderType
from .execution_handler import ExecutionHandler
from queue import Queue
from baxter.event import Event, EventType
from baxter.event.fill import FillEvent
import datetime
from typing import cast, Literal, TypedDict
from saxo_openapi import OpenAPIError, API
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.session import account_info
from saxo_openapi.contrib.util import InstrumentToUic
import os
import aiohttp
import asyncio

# there aren't separate execution handlers for sim and live saxo accounts, as these will be distinquished by the API token, I think


class SaxoOrder(TypedDict):
    AssetType: Literal["Stock"]
    Uic: int
    AccountKey: str
    Amount: int
    BuySell: Literal["Buy", "Sell"]
    OrderType: Literal["Market", "Limit"]
    ManualOrder: bool


class SaxoExecutionHandler(ExecutionHandler):

    def __init__(self, events: Queue[Event]) -> None:

        self.events = events

        self._set_saxo_api()

        # self.client = aiohttp.ClientSession(
        #    base_url=self.base_url, headers=self.headers)

        self.acct_key = asyncio.run(self._get_acct_key())

    def _set_saxo_api(self):
        self.saxo_token = os.environ.get('SAXO_API')
        self.headers = {
            'Accept-Encoding': 'deflate, gzip',
            'Authorization': f'Bearer {self.saxo_token}',
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://gateway.saxobank.com/sim/'

    async def _get_acct_key(self):
        async with aiohttp.ClientSession(
                base_url=self.base_url, headers=self.headers) as session:
            async with session.get('openapi/port/v1/accounts/me') as response:
                return await response.json()

    def _create_saxo_order(self, order: OrderEvent) -> SaxoOrder:

        spec = {
            "Instrument": order.symbol,
            "Amount": order.quantity,
            "BuySell": "Buy" if order.direction == "BUY" else "Sell",
            "OrderType": "Market" if order.order_type.name == 'MKT' else "Limit",
            "ManualOrder": True
        }

        spec_with_uic = InstrumentToUic(
            client=self.client, AccountKey=acct_key, spec=spec, assettype="Stock")

        return SaxoOrder(AccountKey=acct_key, AssetType="Stock", **spec_with_uic)

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
            order = self._create_saxo_order(event)
            order = tr.orders.Order(data=order)
            self.client.request(order)
