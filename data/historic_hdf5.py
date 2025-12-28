from queue import Queue
from .data_handler import DataHandler, BarType
from event.market import MarketEvent
from typing import List, Iterator, Dict, Hashable, Generator
import pandas as pd
import logging
from pathlib import Path
import datetime


class HistoricHDF5DataHandler(DataHandler):
    """
    Docstring for HistoricHDF5DataHandler

    Parameters:
    events: Events Queue object
    hdf5_dir: absolute path to the file
    symbol_list: list of symbols to handle data for

    Additional attributes:
    symbol_data: a dict with symbol as keys and corresponding data as values.
    latest_symbol_data: 
    continue_backtest: bool to signal whether to keep backtesting or not.

    DataHandler for handling historic .h5 files.
    """

    def __init__(self, events: Queue, hdf5_dir: str, symbol_list: List[str]) -> None:
        """
        Docstring for __init__

        :param self: The DataHandler instance.
        :param events: The events Queue object containing the events to which the system reacts.
        :type events: Queue
        :param hdf5_dir: The absolute path representing the location of the directory containing the .h5-file.
        :type hdf5_dir: str
        :param symbol_list: The list of ticker symbols to handle data for.
        :type symbol_list: List[str]
        """

        self.events = events
        self.hdf5_dir = Path(hdf5_dir)
        self._symbol_list = symbol_list

        self.symbol_data: Dict[str,
                               Iterator[tuple[Hashable, pd.Series[float]]]] = {}
        self.latest_symbol_data: Dict[str, List[BarType]] = {}
        self._continue_backtest = True

        self._open_convert_hdf5_files()

    @property
    def symbol_list(self):
        return self._symbol_list

    @property
    def continue_backtest(self) -> bool:
        return self._continue_backtest

    @continue_backtest.setter
    def continue_backtest(self, new_setting: bool) -> None:
        if isinstance(new_setting, bool):
            self._continue_backtest = new_setting
        else:
            return TypeError("continue_backtest must be a boolean.")

    def update_bars(self) -> None:
        """
        Docstring for update_bars

        :param self: Instance of DataHandler

        Updates the self.latest_symbol_data attributes
        with the latest bar for each ticker symbol.
        """

        # iterate over each symbol and check if a new bar is available. If not, then stop the backtest.
        for symbol in self.symbol_list:
            try:
                bar = next(self._get_new_bar(symbol))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)

        # when each symbol has its latest bar, emit a new MarketEvent to continue the event loop
        self.events.put(MarketEvent())

    def get_latest_bars(self, symbol: str, N=1) -> List[BarType]:
        """
        Docstring for get_latest_bars

        :param self: HistoricHDF5DataHandler instance
        :param symbol: ticker symbol
        :type symbol: str
        :param N: number of bars to get
        :return: list of N bars
        :rtype: List[BarType] | None

        Returns the latest N bars for the given symbol. If less than N bars are
        available, the available number of bars are returned.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("This historical dataset does not contain this symbol.")
            return [(f"unknown ticker: {symbol}", datetime.datetime.now(), 0.0, 0.0, 0.0, 0.0, 0)]
        else:
            return bars_list[-N:]

    def _open_convert_hdf5_files(self) -> None:
        """
        Docstring for _open_convert_hdf5_files

        :param self: The DataHandler instance.

        Private method to open a .h5 file and convert it
        to the desirable format. The method returns nothing
        on its own but generates the self.symbol_data dictionary.
        """

        # comb_index is the eventual combination of all indices of the pd.DataFrames
        comb_index = None
        # for each symbol, create a dict entry with a pd.DataFrame of data
        temp_data: Dict[str, pd.DataFrame | pd.Series] = {}
        for ticker in self.symbol_list:
            with pd.HDFStore(self.hdf5_dir) as store:
                data = store.get(f"price_series/{ticker}")
            data.sort_index(inplace=True)

            # check if comb_index has been set yet, and set it if it hasn't, otherwise combine it with the already defined comb_index
            if comb_index is None:
                comb_index = data.index
            else:
                comb_index.union(data.index)

            # the latest is empty since this method is only called upon instantiation
            self.latest_symbol_data[ticker] = []

            # save the data in a temporary dict
            temp_data[ticker] = data

        # next, reindex and pad the data series on the combined index comb_index, as well as calculating returns
        for ticker in self.symbol_list:
            temp_data[ticker].reindex(index=comb_index, method="ffill")
            temp_data[ticker]["returns"] = temp_data[ticker]["Close"].pct_change(
            ).dropna()

        # compensate for the dropped row from the .dropna above by reindexing on comb_index, and make the dataframes into generators with .iterrows
        for ticker in self.symbol_list:
            self.symbol_data[ticker] = temp_data[ticker].reindex(
                index=comb_index, method="ffill").iterrows()

    def _get_new_bar(self, symbol: str) -> Generator[BarType]:
        """
        Docstring for _get_new_bar

        :param self: HistoricHDF5DataHandler instance
        :param symbol: the relevant ticker symbol
        :type symbol: str
        :return: a row of OHLCV data of the form with a time stamp and ticker symbol
        :rtype: Generator[BarType, None, None]

        Yields a generator containing a single bar of data for the given symbol,
        and corresponding to a single point in time. The columns correspond to
        'Ticker', 'Date', 'Open', 'High', 'Low',  'Close', 'Volume'.
        """
        for datum in self.symbol_data[symbol]:
            row = (symbol, datetime.datetime.strptime(
                str(datum[0]), "%Y-%m-%d %H:%M:%S"), datum[1].iloc[0], datum[1].iloc[1], datum[1].iloc[2], datum[1].iloc[3], datum[1].iloc[4])
            yield row
