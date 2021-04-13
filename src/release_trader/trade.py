"""Run the trade functions based on information gained from the other scripts."""
import configparser

import ccxt

import release_trader.check_availability as ca

# LOGIN_B = cf.BINANCE_DICT
# LOGIN_C = cf.COINBASE_DICT
# LOGIN_CP = cf.COINBASE_PRO_DICT
# LOGIN_G = cf.GATEIO_DICT
# LOGIN_Gv4 = cf.GATEIOv4_DICT
config = configparser.ConfigParser()
config.read_file(open(r"../.user.cfg"))
LOGIN_Gv4 = {
    "API_KEY": config.get("gateio_user_config", "api_key"),
    "SECRET_KEY": config.get("gateio_user_config", "secret_key"),
}
# LOGIN_K = cf.KRAKEN_DICT
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


# def check_balance():
#     """Check balance of accounts and print."""
#     for w, login in zip(websites, LOGINS):
#         class_ = getattr(ccxt, w)
#         exchange = class_({"apiKey": login["API_KEY"], "secret": login["SECRET_KEY"]})
#         balance = exchange.fetch_balance()
#         try:
#             print(balance["total"]["BTC"])
#             print(balance["total"]["XLM"])
#         except Exception:
#             print("Failed try statement")
#             bt = balance["total"]
#             print(bt)


def buy_crypto():
    """Place a buy order with a limit sell order on new coins."""
    _ = ccxt.gateio(
        {"apiKey": LOGIN_Gv4["API_KEY"], "secret": LOGIN_Gv4["SECRET_KEY"]}
    )  # gateio
    _ = ca.new_crypto()  # crypto
    # for symbol in crypto:
    #     time.sleep(gateio.rateLimit / 1000)
    #     gateio.create_market_buy_order(
    #         symbol,  # symbol
    #         100,  # amount (100 USDT)
    #         type='stop_loss_limit',
    #         params={'stopPrice': .95 * }
    #     )
    # gateio.create_order
    # while not gateio.has['fetch_balance']:
    #     time.sleep(.5)
    # bal = gateio.fetch_balance()  # balance
    # for trade in gateio.fetch_my_trades(symbol='LTC/BTC'):
    #     print(trade['info']['rate'])
    #     rate = trade['info']['rate'] * 1.1
    #     print(bal['LTC'])
    #     print(bal['BTC'])

    # gateio.create_limit_sell_order(symbol, amount, price)


if __name__ == "__main__":
    buy_crypto()
    # check_balance()
