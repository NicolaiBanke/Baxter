from types import SimpleNamespace


class BacktestContext(SimpleNamespace):
    def __enter__(self):
        return self

    def __exit__(self):
        pass
