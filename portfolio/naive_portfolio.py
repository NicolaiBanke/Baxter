from event.fill import FillEvent
from event.signal import SignalEvent
from .portfolio import Portfolio
from datetime import datetime
from typing import List, Dict, Union
from queue import Queue
from data.data_handler import DataHandler, BarType
import pandas as pd
from event.market import MarketEvent
from event.event import EventType
from event.signal import SignalType
from event.order import OrderEvent, OrderType


class NaivePortfolio(Portfolio):
    """
    Docstring for NaivePortfolio

    Standard portfolio subclass for naive order handling. 'Naive' in this
    instance means sending and filling orders without taking into account
    any sort of monetary or risk management limitations imposed on the
    portfolio.
    """

    def __init__(self, bars: DataHandler, events: Queue, initial_capital=100_000.0, start_date=datetime.now()) -> None:
        """
        Docstring for __init__

        :param self: Description
        :param bars: Description
        :type bars: DataHandler
        :param events: Description
        :type events: Queue
        :param initial_capital: Description
        :param start_date: Description
        """

        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.initial_capital = initial_capital
        self.start_date = start_date

        self._all_positions = self._construct_all_positions()
        self._current_positions = {s: 0 for s in self.bars.symbol_list}
        self._all_holdings = self._construct_all_holdings()
        self._current_holdings = self._construct_current_holdings()

        self._equity_curve = None

    @property
    def all_positions(self) -> List[Dict[str, Union[int, datetime]]]:
        return self._all_positions

    @property
    def current_positions(self) -> Dict[str, int]:
        return self._current_positions

    @property
    def all_holdings(self) -> List[Dict[str, Union[str, datetime, float]]]:
        return self._all_holdings

    @property
    def current_holdings(self) -> Dict[str, Union[int, float]]:
        return self._current_holdings

    @property
    def equity_curve(self) -> pd.DataFrame | None:
        return self._equity_curve

    @equity_curve.setter
    def equity_curve(self, new_curve: pd.DataFrame) -> None:
        self._equity_curve = new_curve

    def _construct_all_positions(self) -> List[Dict[str, Union[int, datetime]]]:
        """
        Docstring for _construct_all_positions

        :param self: Portfolio instance.
        :return: dictionary with ticker keys and 0 values wrapped in a list.
        :rtype: List[Dict[str, str | datetime]]

        Constructs a list of positions given in a dict with a 'datetime'
        set to self.start_date to note the starting date of the portfolio.
        """

        d: Dict[str, Union[int, datetime]] = {
            s: 0 for s in self.symbol_list
        }
        d['datetime'] = self.start_date

        return [d]

    def _construct_all_holdings(self) -> List[Dict[str, Union[int, datetime, float]]]:
        """
        Docstring for _construct_all_holdings

        :param self: Portfolio instance.
        :return: dictionary with keys: ticker, datetime, cash, commission, total wrapped in a list.
        :rtype: List[Dict[str, int | datetime | float]]

        Constructs all of the holdings in the portfolio, i.e., the amount of money in
        each ticker, along with the amount of money in cash and commission paid.
        The total amount of money is also given in the 'total' entry.
        """

        d: Dict[str, Union[int, datetime, float]] = {
            s: 0 for s in self.symbol_list
        }
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital

        return [d]

    def _construct_current_holdings(self) -> Dict[str, Union[int, float]]:
        """
        Docstring for _construct_current_holdings

        :param self: Portfolio instance.
        :return: dict with the current holdings, so it does not include a 'datetime' entry.
        :rtype: Dict[str, str | float]


        """

        d: Dict[str, Union[int, float]] = {
            s: 0 for s in self.symbol_list
        }
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital

        return d

    def _update_positions_from_fill(self, fill_event: FillEvent) -> None:
        """
        Docstring for _update_positions_from_fill

        :param self: Portfolio instance.
        :param fill_event: FillEvent object which contains information about the fill.
        :type fill_event: FillEvent
        """

        # check the direction of the FillEvent: can only be 'BUY' or 'SELL'
        fill_dir = 1 if fill_event.direction == "BUY" else -1

        # update the positions
        self.current_positions[fill_event.symbol] += fill_dir * \
            fill_event.quantity

    def _update_holdings_from_fill(self, fill_event: FillEvent) -> None:
        """
        Docstring for _update_holdings_from_fill

        :param self: Portfolio instance.
        :param fill_event: FillEvent object which contains information about the fill.
        :type fill_event: FillEvent
        """

        # check the direction of the FillEvent: can only be 'BUY' or 'SELL'
        fill_dir = 1 if fill_event.direction == "BUY" else -1

        # estimate cost of fill by the current Close price
        fill_cost = self.bars.get_latest_bars(fill_event.symbol)[0][5]
        # cost is the amount of money exiting the cash holdings
        cost = fill_cost * fill_dir * fill_event.quantity
        # update the different dict entries accordingly
        self.current_holdings[fill_event.symbol] += cost
        self.current_holdings["commission"] += fill_event.commission
        self.current_holdings["cash"] -= cost + fill_event.commission
        self.current_holdings["total"] -= cost + fill_event.commission

    def _generate_naive_order(self, signal_event: SignalEvent) -> OrderEvent | None:
        """
        Docstring for _generate_naive_order

        :param self: Portfolio instance
        :param signal_event: the SignalEvent generated by a Strategy object
        :type signal_event: SignalEvent
        :return: returns an OrderEvent fulfilling the suggestion from the Strategy object or None if no order is appropriate
        :rtype: OrderEvent | None
        """

        symbol = signal_event.symbol
        direction = signal_event.signal_type
        # strength = signal_event.strength, maybe include a strength attribute

        mkt_quantity = 100  # floor(100*strength)
        cur_quantity = self.current_positions[symbol]
        order_type = OrderType.MKT

        order = None

        # if signal direction is long and there are currently no shares of the given ticker
        if direction == SignalType.LONG and cur_quantity == 0:
            order = OrderEvent(symbol=symbol, direction="BUY",
                               order_type=order_type, quantity=mkt_quantity)
        # if signal direction is short and there are currently no shares of the given ticker
        elif direction == SignalType.SHORT and cur_quantity == 0:
            order = OrderEvent(symbol=symbol, direction="SELL",
                               order_type=order_type, quantity=mkt_quantity)

        # if signal direction is exit and we are currently long shares of the given ticker
        elif direction == SignalType.EXIT and cur_quantity > 0:
            order = OrderEvent(symbol=symbol, direction="SELL",
                               order_type=order_type, quantity=mkt_quantity)
        # if signal direction is short and we are currently short shares of the given ticker
        elif direction == SignalType.SHORT and cur_quantity < 0:
            order = OrderEvent(symbol=symbol, direction="BUY",
                               order_type=order_type, quantity=abs(mkt_quantity))

        return order

    def create_equity_curve_dataframe(self) -> None:
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
        self.equity_curve = curve

    def update_timeindex(self, event: MarketEvent) -> None:
        """
        Docstring for update_timeindex

        :param self: Portfolio instance
        :param event: the current MarketEvent
        :type event: MarketEvent

        Updates the positions and holdings of the portfolio
        at each MarketEvent.
        """
        bars: Dict[str, List[BarType]] = {}
        for ticker in self.symbol_list:
            bars[ticker] = self.bars.get_latest_bars(ticker)

        # get and append current positions
        dp = {**self.current_positions,
              'datetime': bars[self.symbol_list[0]][0][1]}
        self.all_positions.append(dp)

        # get and append current holdings
        dh = {**self.current_holdings,
              'datetime': bars[self.symbol_list[0]][0][1]}

        for ticker in self.symbol_list:
            # approximate the market value using the volume
            market_value = self.current_positions[ticker] * bars[ticker][0][5]
            dh[ticker] = market_value
            dh['total'] += market_value

        self.all_holdings.append(dh)

    def update_fill(self, fill_event: FillEvent) -> None:
        """
        Docstring for update_fill

        :param self: Portfolio instance
        :param fill_event: the received FillEvent
        :type fill_event: FillEvent

        Updates the portfolio holdings and positions upon
        receiving a FillEvent.
        """
        if fill_event.type == EventType.FILL:
            self._update_positions_from_fill(fill_event)
            self._update_holdings_from_fill(fill_event)

    def update_signal(self, signal_event: SignalEvent) -> None:
        """
        Docstring for update_signal

        :param self: Portfolio instance
        :param signal_event: the signal received from the Strategy object
        :type signal_event: SignalEvent

        Responds to the SignalEvent by generating a naive order, and puts
        the resulting OrderEvent on the events queue.
        """

        if signal_event.type == EventType.SIGNAL:
            order_event = self._generate_naive_order(signal_event)
            self.events.put(order_event)
