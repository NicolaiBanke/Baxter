from inspect import isgenerator
from evbax.data.historic_hdf5 import HistoricHDF5DataHandler
from queue import Queue


def test__open_convert_hdf5_files(data_handler_args):
    h5dh = HistoricHDF5DataHandler(*data_handler_args)
    h5dh._open_convert_hdf5_files()

    assert isgenerator(list(h5dh.symbol_data.values())[0])


def test__get_new_bar(data_handler_args):
    h5dh = HistoricHDF5DataHandler(*data_handler_args)
    assert isgenerator(h5dh._get_new_bar(data_handler_args[-1][0]))


def test_get_latest_bars(data_handler_args):
    h5dh = HistoricHDF5DataHandler(*data_handler_args)
    bars = h5dh.get_latest_bars(data_handler_args[0])

    assert isinstance(bars, list | None)


def test_update_bars_put_marketevent(events_queue, data_handler_args):
    before_size = data_handler_args[0].qsize()
    h5dh = HistoricHDF5DataHandler(*data_handler_args)
    h5dh.update_bars()
    assert events_queue.qsize() == before_size + 1


def test_update_bars_sets_latest_symbol_data(events_queue, data_handler_args):
    h5dh = HistoricHDF5DataHandler(*data_handler_args)
    try:
        before_size = len(list(h5dh.latest_symbol_data.values())[0])
    except IndexError:
        before_size = 0

    h5dh.update_bars()
    assert len(list(h5dh.latest_symbol_data.values())[0]) == before_size + 1
