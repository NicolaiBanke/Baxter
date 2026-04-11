from baxter.event.order import OrderEvent
from baxter.execution.execution_handler import AsyncExecutionHandler
from queue import Queue
from baxter.event import Event
from baxter.event.fill import FillEvent
import datetime
from typing import Literal, TypedDict
import os
import aiohttp
import asyncio
import logging
from tools.logging_conf import errHandler, stdoutHandler
import json
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(stdoutHandler)
logger.addHandler(errHandler)

# there aren't separate execution handlers for sim and live saxo accounts, as these will be distinquished by the API token, I think


class SaxoOrder(TypedDict):
    AssetType: Literal["Stock"]
    Uic: int
    AccountKey: str
    Amount: int
    BuySell: Literal["Buy", "Sell"]
    OrderType: Literal["Market", "Limit"]
    ManualOrder: bool


class SaxoExecutionHandler(AsyncExecutionHandler):
    def __init__(self, events: Queue[Event]) -> None:

        self.events = events

        self._set_saxo_api()

        self.acct_key = asyncio.run(self._get_acct_key())

    def _set_saxo_api(self):
        self.saxo_token = os.environ.get("SAXO_API")
        self.headers = {
            "Accept-Encoding": "deflate, gzip",
            "Authorization": f"Bearer {self.saxo_token}",
            "Content-Type": "application/json",
        }
        self.base_url = "https://gateway.saxobank.com/sim/"

    async def _get_acct_key(self):
        async with aiohttp.ClientSession(
            base_url=self.base_url, headers=self.headers
        ) as session:
            async with session.get("openapi/port/v1/accounts/me") as response:
                res = await response.json()

        return res["Data"][0]["AccountKey"]

    async def _create_saxo_order(
        self, order: OrderEvent, session: aiohttp.ClientSession
    ) -> SaxoOrder:
        spec = {
            "Instrument": order.symbol,
            "Amount": order.quantity,
            "BuySell": "Buy" if order.direction == "BUY" else "Sell",
            "OrderType": "Market" if order.order_type.name == "MKT" else "Limit",
            "ManualOrder": True,
        }

        async with session.get(
            url=f"openapi/ref/v1/instruments?AssetTypes=Stock&Keywords={spec.get('Instrument', '')}"
        ) as response:
            res = await response.json()

        if len(res["Data"]) == 1:
            del spec["Instrument"]
            spec.update({"Uic": res["Data"][0]["Identifier"]})
        else:
            raise ValueError(
                "Got multiple instruments for: {}".format(spec["Instrument"])
            )

        saxo_order_args: dict[str, str | int] = {
            "AccountKey": self.acct_key,
            "AssetType": "Stock",
            **spec,
        }

        saxo_order: SaxoOrder = {**saxo_order_args}

        return saxo_order

    # should possibly be public method
    def _create_fill(self, event: FillEvent):
        # should put fill event on queue when .execute_order gets confirmation that the order went through
        fill_event = FillEvent(
            direction=event.direction,
            exchange="ARCA",
            fill_cost=None,
            quantity=event.quantity,
            symbol=event.symbol,
            time_index=pd.Timestamp.now(datetime.timezone.utc),
        )

        self.events.put(fill_event)
        raise NotImplementedError

    async def execute_order(
        self, event: OrderEvent, session: aiohttp.ClientSession
    ) -> aiohttp.ClientResponse:
        # if event.type == EventType.ORDER: <-- this gets in the way of type checking for a client response
        saxo_order = await self._create_saxo_order(event, session=session)
        data = json.dumps(saxo_order)
        async with session.post(
            "openapi/trade/v2/orders", headers=self.headers, data=data
        ) as response:
            # not sure if I want to return a Response object, which can be checked for status, or an await'ed .json object
            return response
