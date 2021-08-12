"""Check if websites trade new coins and return valid coins."""
import logging
import sys

import ccxt

import release_trader.webscaper as ws

websites = [
    # 'binance',
    # 'coinbase',
    "gateio",
    # 'kraken'
]

logging.basicConfig(
    level=logging.INFO,
)
log_formatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
root_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("{0}/{1}.log".format(".", "release_trader"))
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.DEBUG)
root_logger.addHandler(console_handler)


def check_websites(
    crypto: list[str], verbose: bool = False, testing: bool = False
) -> list[str]:
    """Check if websites (gate.io) lists the newly found coins.

    Args:
        crypto: list
            List of coins to check if they are tradeable on gate.io.
        verbose: bool
            If True, print what is going on in more detail
        testing: bool
            Do not write to the history file if the test suit is calling the function

    Returns:
        pairs: list
            List containing the available pairs: USDT or ETH with new coin
    """
    found = []
    pairs = []
    for w in websites:
        try:
            e = getattr(ccxt, w)()
            if verbose:
                print(f"Searching among {len(e.load_markets())} markets on {w}...")
            for m in e.load_markets():
                msp = m.split("/")
                if "USDT" in msp[1]:
                    if msp[0] in crypto:
                        print(f"Found {m}, ready to trade!")
                        found.append(msp[0])
                        pairs.append(m)
            print(f"No mathch for coin(s) {list(set(crypto) - set(found))}")
        except Exception:
            root_logger.warning(f"Could not get markets/list of coins from {w}")
    # TODO: history.txt should perhaps be binary/zipped so it is harder to change it.
    with open("src/release_trader/history.txt", "a") as f:
        allready_in = list(
            line.strip() for line in open("src/release_trader/history.txt")
        )
        for found_coin in crypto:
            if found_coin not in allready_in and not testing:
                f.write(f"{found_coin}\n")
    return pairs


def new_crypto(verbose=False, test_coin: str = "none") -> list[str]:
    """Check if coins have been traded allready.

    A history file listing all coins that have been found by the program is
    check, in addition to binance and coinbase themselves.

    Args:
        verbose: bool
            If True, print more info.
        test_coin: str
            Used within the test suite. Send in a dummy coin to see if it is removed

    Returns:
        list: Coins that are new to the program.
    """
    # Get the newly listed crypto from both websites and combine
    if test_coin == "none":
        crypto_b = ws.navigate_binance()
        crypto_c = ws.navigate_coinbase()
        crypto = crypto_b + crypto_c
    else:
        crypto = [test_coin]

    # Check the history file
    allready_in = {line.strip() for line in open("src/release_trader/history.txt")}
    intersect = allready_in & set(crypto)
    new_coin = []
    if len(intersect) == 0:
        new_coin = crypto
    else:
        for item in set(crypto) - intersect:
            new_coin.append(item)

    # Check binance and coinbase
    for w in ["binance", "coinbase"]:
        try:
            e = getattr(ccxt, w)()
            markets = set(e.load_markets())
            for coin in new_coin:
                if f"{coin}/USDT" in markets:
                    new_coin.remove(coin)
        except Exception:
            root_logger.warning(f"Could not get markets/list of coins from {w}")

    # Check if the coins are listed on gateio and more, then return coins that
    # are tradeable
    if len(new_coin) != 0:
        found = check_websites(new_coin)
        return found
    if verbose:
        print("found nothing new")
    return []


if __name__ == "__main__":
    print("check_availability.__main__")
    print(new_crypto())
