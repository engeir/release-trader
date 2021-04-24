"""Tests for the check_availability module."""
import release_trader.check_availability as ca


def test_check_websites():
    """Test for function check_websites."""
    btc = ["BTC"]
    assert ca.check_websites(btc, testing=True) == ["BTC/USDT"]
    nonsense = ["NONSENSECOIN"]
    assert ca.check_websites(nonsense, testing=True) == []


def test_new_crypto():
    """Test for function new_crypto."""
    test_coin = "BTC"
    assert ca.new_crypto(test_coin) == []
