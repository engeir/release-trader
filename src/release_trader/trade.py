"""Run the trade functions based on information gained from the other scripts."""
import ccxt
import check_availability as ca
import config as cf

LOGIN_B = cf.BINANCE_DICT
LOGIN_C = cf.COINBASE_DICT
LOGIN_CP = cf.COINBASE_PRO_DICT
LOGIN_G = cf.GATEIO_DICT
LOGIN_Gv4 = cf.GATEIOv4_DICT
LOGIN_K = cf.KRAKEN_DICT
LOGINS = [
    # LOGIN_B,
    # LOGIN_C,
    # LOGIN_CP,
    # LOGIN_G,
    LOGIN_Gv4,
    # LOGIN_K
]
websites = [
    # 'binance',
    # 'coinbase',
    # 'coinbasepro',
    # 'gateio',
    "gateio",
    # 'kraken'
]

if len(LOGINS) != len(websites):
    print("Need one login per website.")
    raise AssertionError


def list_markets():
    """Print out all available trades from 'websites'."""
    for w in websites:
        e = getattr(ccxt, w)()
        print(f"Number of markets for {e}")
        print(len(e.load_markets()))
        # c = 0
        # for m in e.load_markets():
        #     print(m)
        #     c += 1
        # print(c)
        # print(e.load_markets())


def check_balance():
    """Check balance of accounts and print."""
    for w, login in zip(websites, LOGINS):
        class_ = getattr(ccxt, w)
        exchange = class_({"apiKey": login["API_KEY"], "secret": login["SECRET_KEY"]})
        balance = exchange.fetch_balance()
        try:
            print(balance["total"]["BTC"])
            print(balance["total"]["XLM"])
        except Exception:
            print("Failed try statement")
            bt = balance["total"]
            print(bt)


def buy_crypto():
    """Place a buy order with a limit sell order on new coins."""
    gateio = ccxt.gateio(
        {"apiKey": LOGIN_Gv4["API_KEY"], "secret": LOGIN_Gv4["SECRET_KEY"]}
    )
    _ = gateio.fetch_balance()  # balance
    _ = ca.new_crypto()  # crypto
    # for coinpair in crypto:
    #     gateio.create_market_buy_order(
    #         coinpair,
    #     )
    # gateio.create_limit_sell_order(symbol, amount, price)


if __name__ == "__main__":
    check_balance()
