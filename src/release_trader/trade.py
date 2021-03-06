"""Run the trade functions based on information gained from the other scripts."""
import configparser

import ccxt

# import time
# from threading import Timer

# import release_trader.check_availability as ca

# import logging

# import gate_api

config = configparser.ConfigParser()
config.read_file(open(r"../.user.cfg"))
LOGIN_Gv4 = {
    "API_KEY": config.get("gateio_user_config", "api_key"),
    "SECRET_KEY": config.get("gateio_user_config", "secret_key"),
}


def ratelimit():
    """Print the rate limit of API calls."""
    gateio = ccxt.gateio(
        {"apiKey": LOGIN_Gv4["API_KEY"], "secret": LOGIN_Gv4["SECRET_KEY"]}
    )  # gateio
    print(gateio.rateLimit)


def buy_crypto():
    """Place a buy order with a limit sell order on new coins."""
    pass
    # gateio = ccxt.gateio(
    #     {"apiKey": LOGIN_Gv4["API_KEY"], "secret": LOGIN_Gv4["SECRET_KEY"]}
    # )  # gateio
    # crypto = ca.new_crypto()  # crypto

    # Here we want to buy the currency we found as a market buy order with a
    # stop loss. We can potentially (actually it is very likely) buy several
    # coins at the same time (might as well trash all but one?)
    # for symbol in crypto:
    #     # time.sleep(gateio.rateLimit / 1000)  # The rateLimit is 1000
    #     time.sleep(1)
    # OLD
    # for symbol in crypto:
    #     time.sleep(gateio.rateLimit / 1000)
    #     gateio.create_market_buy_order(
    #         symbol,  # symbol
    #         100,  # amount (100 USDT)
    #         type='stop_loss_limit',
    #         params={'stopPrice': .95 * }
    #     )

    # After we have bought something we want to check if the price of our new
    # coin(s) has increased with at least 10 %
    # while not gateio.has['fetch_balance']:
    #     time.sleep(.5)
    # bal = gateio.fetch_balance()  # balance
    # for trade in gateio.fetch_my_trades(symbol='LTC/BTC'):
    #     print(trade['info']['rate'])
    #     rate = trade['info']['rate'] * 1.1
    #     if rate < the_current_price:
    #         gateio.create_limit_sell_order('coin_that_is_available')
    #     print(bal['LTC'])
    #     print(bal['BTC'])

    # gateio.create_limit_sell_order(symbol, amount, price)

    # This will call this function again in five seconds.
    # Timer(5, buy_crypto).start()


if __name__ == "__main__":
    ratelimit()
    # buy_crypto()
