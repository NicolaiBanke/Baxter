from queue import Queue, Empty
from baxter.event.event import Event, EventType
from baxter.data.historic_hdf5 import HistoricHDF5DataHandler

data_path = "/home/n1c0/Dropbox/Quant/Projects/baxter/tests"
symbols = ["SPY", "QQQ"]

events: Queue[Event] = Queue()

bars = HistoricHDF5DataHandler(
    events, data_path + "/test_hdf5data.h5", symbols)
# strategy = Strategy()
# port = Portfolio()
# broker = ExecutionHandler()


# the loop representing market events
def main():
    while bars.continue_backtest:
        bars.update_bars()

        # handle the incoming events one by one
        while True:
            try:
                event = events.get(False)
            except Empty:
                break
            else:
                if event is not None:
                    if event.type == EventType.MKT:
                        # strategy.calculate_signals(event)
                        # # port.update_timeindex(event)
                        bars.continue_backtest = False


if __name__ == "__main__":
    main()
