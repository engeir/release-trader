"""This script implements simple functions that talk with gateio.

The functions are responsible for buying and trading through gate.io's API.
"""
import configparser
import hashlib
import hmac
import logging
import sys
import time

import requests
from gate_api import ApiClient
from gate_api import Configuration
from gate_api import SpotApi

# from decimal import Decimal as D
# from gate_api import Order

# from config import RunConfig

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

config = configparser.ConfigParser()
config.read_file(open(r"../.user.cfg"))
LOGIN_Gv4 = {
    "API_KEY": config.get("gateio_user_config", "api_key"),
    "SECRET_KEY": config.get("gateio_user_config", "secret_key"),
}


def gen_sign(method, url, query_string=None, payload_string=None):
    """Generate signature used with the gateio API."""
    key = LOGIN_Gv4["API_KEY"]  # api_key
    secret = LOGIN_Gv4["SECRET_KEY"]  # api_secret

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode("utf-8"))
    hashed_payload = m.hexdigest()
    s = "%s\n%s\n%s\n%s\n%s" % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(
        secret.encode("utf-8"), s.encode("utf-8"), hashlib.sha512
    ).hexdigest()
    return {"KEY": key, "Timestamp": str(t), "SIGN": sign}


def list_spot_accounts() -> list:
    """Check your spot account.

    Returns:
        list:
            A list of lists. Each inner list has length of two, with the first
            element being the coin and the second the available amount in the spot
            wallet.

    Examples:
    >>> list_spot_accounts()
    [["BTC", 0.002], ["USDT", 45.013]]
    """
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url = "/spot/accounts"
    query_param = ""
    # for `gen_sign` implementation, refer to section `Authentication` above
    sign_headers = gen_sign("GET", prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request("GET", host + prefix + url, headers=headers)
    spot_account = []
    spot_account_app = spot_account.append
    for currency in r.json():
        # We do not want to touch the GT account, used to pay cheaper fees
        if currency["currency"] != "GT":
            spot_account_app([currency["currency"], currency["available"]])
        # print(currency["currency"] + "\t" + currency["available"])
    return spot_account


def move_spot_usdt_to_btc() -> None:
    """Move all available USDT to BTC at the last price found on GateIo."""
    root_logger.info("Moving all USDT to BTC on spot account")
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url = "/spot/orders"
    query_param = ""
    spots = list_spot_accounts()
    for account in spots:
        if account[0] == "USDT":
            last_price = get_last_price("BTC_USDT")
            body1 = '{"text":"t-123456","currency_pair":"BTC'
            # The "side" refers to the first coin in the currency pair
            body2 = (
                '_USDT","type":"limit","account":"spot","side":"buy",'
                + '"iceberg":"0","amount":"'
            )
            body3 = '","price":"'
            body4 = '","time_in_force":"gtc","auto_borrow":false}'
            body = (
                body1
                + body2
                + str(float(account[1]) / float(last_price))
                + body3
                + str(last_price)
                + body4
            )
            sign_headers = gen_sign("POST", prefix + url, query_param, body)
            headers.update(sign_headers)
            _ = requests.request(
                "POST", host + prefix + url, headers=headers, data=body
            )
            # print(r.json())


def move_all_spot_to_btc():
    """Move all coins to BTC at the last price found on GateIo."""
    root_logger.info("Moving all spot accounts to BTC")
    move_all_spot_to_usdt()
    move_spot_usdt_to_btc()


def move_all_spot_to_usdt() -> None:
    """Move all coins to USDT at the last price found on GateIo."""
    root_logger.info("Moving all spot accounts to USDT")
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url = "/spot/orders"
    query_param = ""
    spots = list_spot_accounts()
    for account in spots:
        if account[0] != "USDT":
            last_price = get_last_price(str(account[0]) + "_USDT")
            body1 = '{"text":"t-123456","currency_pair":"'
            # The "side" refers to the first coin in the currency pair
            body2 = (
                '_USDT","type":"limit","account":"spot","side":"sell",'
                + '"iceberg":"0","amount":"'
            )
            body3 = '","price":"'
            body4 = '","time_in_force":"gtc","auto_borrow":false}'
            body = (
                body1
                + str(account[0])
                + body2
                + str(account[1])
                + body3
                + str(last_price)
                + body4
            )
            sign_headers = gen_sign("POST", prefix + url, query_param, body)
            headers.update(sign_headers)
            _ = requests.request(
                "POST", host + prefix + url, headers=headers, data=body
            )
            # print(r.json())


def get_last_price(pair) -> float:
    """Get the last price of a coin pair.

    The last coin gives the unit, i.e. for the pair "LTC_USDT", the function will return
    the price of one LTC in USDT, which essentially is dollar.

    Args:
        pair: str
            A coin pair that follow gate.io's format. See examples.

    Returns:
        float:
            The current price of the first coins in the pair, given in units of the
            second coin

    Examples:
    >>> get_last_price("BTC_USDT")
    143.02
    """
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    url = "/spot/accounts"
    query_param = ""
    if "/" in pair:
        pair_list = pair.split("/")
        pair = f"{pair_list[0]}_{pair_list[1]}"
    # for `gen_sign` implementation, refer to section `Authentication` above
    sign_headers = gen_sign("GET", prefix + url, query_param)
    config = Configuration(
        key=sign_headers["KEY"], secret=sign_headers["SIGN"], host=host + prefix
    )
    spot_api = SpotApi(ApiClient(config))
    tickers = spot_api.list_tickers(currency_pair=pair)
    # assert len(tickers) == 1
    last_price = tickers[0].last
    # Multiplying with 1.1 to buy up faster
    return float(last_price) * 1.1


def buy_coin_with_usdt(coin: str) -> float:
    """Buy a coin listed by GateIo using your USDT account.

    This will buy with all USDT available at the last price found at GateIo's
    exchange.

    Args:
        coin: str
            The coin you want to buy

    Returns:
        float:
            The price of the coin you are buying, given in USDT

    Examples:
    >>> buy_coin_with_usdt("LTC")
    144.02
    """
    root_logger.info("Moving all USDT to `coin` on spot account")
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url = "/spot/orders"
    query_param = ""
    spots = list_spot_accounts()
    last_price = 0.0
    for account in spots:
        if account[0] == "USDT":
            last_price = get_last_price(str(coin) + "_USDT")
            body1 = '{"text":"t-123456","currency_pair":"'
            # The "side" refers to the first coin in the currency pair
            body2 = (
                '_USDT","type":"limit","account":"spot","side":"buy",'
                + '"iceberg":"0","amount":"'
            )
            body3 = '","price":"'
            body4 = '","time_in_force":"gtc","auto_borrow":false}'
            body = (
                body1
                + str(coin)
                + body2
                + str(float(account[1]) / float(last_price))
                + body3
                + str(last_price)
                + body4
            )
            sign_headers = gen_sign("POST", prefix + url, query_param, body)
            headers.update(sign_headers)
            _ = requests.request(
                "POST", host + prefix + url, headers=headers, data=body
            )
            # print(r.json())
    return last_price


if __name__ == "__main__":
    print(get_last_price("LTC_USDT"))
    # buy_coin_with_usdt("LTC")
    # move_all_spot_to_usdt()
    # get_last_price("BTC_USDT")
