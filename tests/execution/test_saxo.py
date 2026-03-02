from baxter.execution.saxo import SaxoExecutionHandler

def test_execute_order(events_queue, mkt_order):
    saxo_eh = SaxoExecutionHandler(events=events_queue)
    saxo_eh.execute_order(event=mkt_order)
    assert saxo_eh.response == 200