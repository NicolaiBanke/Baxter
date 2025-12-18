from baxter.strategy.strategy import Strategy


def test_strategy_base_class():
    assert "calculate_signals" in Strategy.__abstractmethods__
