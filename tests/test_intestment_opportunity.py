import pytest

from market_watcher.common import MarketWatcherEngine


def mock_threashold_config():
    """Mocks trategy alert configuration."""
    pnl_threashold = {}
    pnl_threashold["LONG_THRESHOLD"] = 5
    pnl_threashold["SHORT_THRESHOLD"] = 0.5
    return pnl_threashold


def mock_get_daily_pnls():
    """Mock fetching of daily P&Ls."""
    return {
        "ABEO": 7.59,
        "ACRX": 4,
        "TPCO": 0.3,
        "TTMI": 0.6,
    }


@pytest.fixture
def mock_target_stocks():
    """Mocks target stocks."""
    print("mock_target_stocks")
    return {
        "ABEO": {"strategy": "long straddle"},
        "ACRX": {"strategy": "long straddle"},
        "TPCO": {"strategy": "short straddle"},
        "TTMI": {"strategy": "short straddle"},
    }


def test_threashold(monkeypatch, mock_target_stocks):
    """Tests if MarketWatcherEngine correctly reports stocks."""

    # Mock fetching data from Yahoo Finance
    monkeypatch.setattr(
        "market_watcher.common.MarketWatcherEngine.get_daily_pnls",
        lambda dummy: mock_get_daily_pnls(),
    )

    # Mock alert threashold config
    monkeypatch.setattr(
        "market_watcher.common.get_pnl_threashold_config",
        lambda: mock_threashold_config(),
    )

    engine = MarketWatcherEngine(mock_target_stocks)
    investment_opportunities = engine.process_latest_market_movements()

    assert "ABEO" in investment_opportunities["long straddle"]
    assert "TPCO" in investment_opportunities["short straddle"]
    assert "ACRX" not in investment_opportunities["long straddle"]
    assert "TTMI" not in investment_opportunities["short straddle"]
