"""Implements the trading strategy for coin releases."""
import configparser
import logging
import sys
import time

import release_trader.check_availability as ca
import release_trader.gateio_functions as gfunc

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
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())

config = configparser.ConfigParser()
config.read_file(open(r"../.user.cfg"))
LOGIN_Gv4 = {
    "API_KEY": config.get("gateio_user_config", "api_key"),
    "SECRET_KEY": config.get("gateio_user_config", "secret_key"),
}


def buy_on_release() -> None:
    """Buy a newly released coin.

    If a new coin is released on Binance of Coinbase and it exists at GateIo, buy.
    If a coin has already been bought, check the current price and sell if it has
    increased or decreased sufficiently.

    """
    # gateio = ccxt.gateio(
    #     {"apiKey": LOGIN_Gv4["API_KEY"], "secret": LOGIN_Gv4["SECRET_KEY"]}
    # )  # gateio
    root_logger.info("Checking for new coins.")
    crypto = ca.new_crypto()

    # Here we want to buy the currency we found as a market buy order with a
    # stop loss. We can potentially (actually it is very likely) buy several
    # coins at the same time (might as well trash all but one?)

    with open("src/release_trader/open_trade.txt", "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    if len(crypto) > 0 and content[0] == "No open trades":
        gfunc.move_all_spot_to_usdt()
        for symbol in crypto:
            # time.sleep(gateio.rateLimit / 1000)  # The rateLimit is 1000
            time.sleep(1)
            s_pair = symbol.split("/")
            coin = s_pair[0] if s_pair[0] != "USDT" else s_pair[1]
            price = gfunc.buy_coin_with_usdt(coin)
            root_logger.info(f"Bought {symbol}. Writing to open_trade.txt")
            with open("src/release_trader/open_trade.txt", "w") as f:
                # The coin I am buying is written to a file for easy access when I am
                # about to sell. There has to be a better way, but it works.
                f.write(f"{coin}\n")
                f.write(str(price))
            break

    # After we have bought something we want to check if the price of our new
    # coin(s) has increased with at least 10 %
    with open("src/release_trader/open_trade.txt", "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    if content[0] == "No open trades":
        pass
    else:
        target_price = float(content[1]) * 1.1
        if target_price < gfunc.get_last_price(f"{content[0]}_USDT"):
            root_logger.info(
                f"The current price of {content[0]} is above ten percent of the"
                + "buy price!"
            )
            gfunc.move_all_spot_to_btc()
            with open("src/release_trader/open_trade.txt", "w") as f:
                f.write("No open trades")
        elif float(content[1]) * 0.95 > gfunc.get_last_price(f"{content[0]}_USDT"):
            root_logger.info(
                f"The price of {content[0]} has dropped with more than five"
                + "percent. Sell."
            )
            gfunc.move_all_spot_to_btc()
            with open("src/release_trader/open_trade.txt", "w") as f:
                f.write("No open trades")


if __name__ == "__main__":
    buy_on_release()
