"""Run the trade functions based on information gained from the other scripts."""
import configparser

import ccxt

import release_trader.check_availability as ca

config = configparser.ConfigParser()
config.read_file(open(r"../.user.cfg"))
LOGIN_Gv4 = {
    "API_KEY": config.get("gateio_user_config", "api_key"),
    "SECRET_KEY": config.get("gateio_user_config", "secret_key"),
}


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
