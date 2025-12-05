import pytest
from datetime import datetime


# arguments for a generic FillEvent object
@pytest.fixture
def fill_args():
    # symbol, quantity, direction, exchange, fill_cost, time_index
    return ["symbol", 1, "BUY", "exchange", 1.0, datetime.now()]

# arguments for a generic OrderEvent object


@pytest.fixture
def order_args():
    # symbol, quantity, direction, order_type
    return ["symbol", 1, "BUY", "MKT"]
