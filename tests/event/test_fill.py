from evbax.event.fill import FillEvent


def test_has_type_fill():
    fe = FillEvent()
    assert fe.type == "FILL"
