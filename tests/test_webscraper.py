"""Tests for the webscraper module."""
import release_trader.webscaper as ws


def test_binance_request():
    """Test for function navigate_binance()."""
    assert isinstance(ws.navigate_binance(), list)
    assert ws.navigate_binance(check=True)[0]
