"""Check if websites trade new coins and return valid coins."""
import ccxt
import webscaper as ws

websites = [
    # 'binance',
    # 'coinbase',
    "gateio",
    # 'kraken'
]


def check_websites(crypto: list) -> list:
    """Check if websites (gate.io) lists the newly found coins.

    Args:
        crypto: List of coins to check if they are tradeable on gate.io.

    Returns:
        list: List containing the available pairs: USDT or ETH with new coin
    """
    found = []
    pairs = []
    for w in websites:
        e = getattr(ccxt, w)()
        print(f"Searching among {len(e.load_markets())} markets on {w}...")
        for m in e.load_markets():
            msp = m.split("/")
            if "USDT" in msp[1]:
                if msp[0] in crypto:
                    print(f"Found {m}, ready to trade!")
                    found.append(msp[0])
                    pairs.append(m)
            elif "ETH" in msp[1]:
                if msp[0] in crypto:
                    print(f"Found {m}, ready to trade!")
                    found.append(msp[0])
                    pairs.append(m)
        print(f"No mathch for coin(s) {list(set(crypto) - set(found))}")
    # TODO: history.txt should perhaps be binary/zipped so it is harder to change it.
    with open("src/release_trader/history.txt", "w") as f:
        allready_in = list(
            line.strip() for line in open("src/release_trader/history.txt")
        )
        for found_coin in crypto:
            if found_coin not in allready_in:
                f.write(found_coin + "\n")
    return pairs


def new_crypto(verbose=False) -> list:
    """Check if coins have been traded allready by checking history file.

    Args:
        verbose: If True, print more info.

    Returns:
        list: Coins that are new to the program.
    """
    crypto_b = ws.navigate_binance()
    crypto_c = ws.navigate_coinbase()
    crypto = crypto_b + crypto_c if not len(crypto_b) == len(crypto_c) == 0 else None
    allready_in = {line.strip() for line in open("src/release_trader/history.txt")}
    crypto_test = set(crypto)
    intersect = list(allready_in & crypto_test)
    new_coin = []
    if len(intersect) == 0:
        new_coin = crypto
    else:
        for item in intersect:
            if item not in crypto:
                new_coin.append(item)
    if len(new_coin) != 0:
        found = check_websites(new_coin)
        return found
    if verbose:
        print("found nothing new")
    return []


if __name__ == "__main__":
    print(new_crypto())
