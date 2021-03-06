"""Scrape the web sites of Binance and Coinbase.

New coins that will be available for trading are announced on two web sites
run by Binance and Coinbase, which are scraped continuously to quickly
buy these on Gate.io and sell them with profit from the hype.
"""
import logging
import re
import sys
from datetime import datetime
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

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


def navigate_binance(verbose: bool = False, check: bool = False) -> list[str]:
    """Navigate to Binance's web page where new coins are announced.

    Args:
        verbose: bool
            Print info about what is found
        check: bool
            Check if the request was successful without errors

    Returns:
        crypto: list[str]
            List of crypto currencies found on binance's website
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) "
        + "Gecko/20100101 Firefox/7.0.1"
    }
    try:
        results = requests.get(
            "https://www.binance.com/en/support/announcement/c-48", headers=headers
        )
    except Exception:
        return []
    if check:
        return [str(results.ok)]
    src = results.content
    soup = BeautifulSoup(src, "lxml")
    if soup.find("a", class_="css-1ej4hfo") is None:
        txt = ""
    else:
        txt = soup.find("a", class_="css-1ej4hfo").text.upper()
    crypto = []
    if "WILL LIST" in txt:
        for t in txt.split():
            if "(" in t:
                crypto.append(str("".join(re.split("[^a-zA-Z]*", t))))
        if verbose:
            print(f"Binance is listing {crypto}!")
    root_logger.info(f"{crypto = }")
    return crypto


def navigate_coinbase(verbose: bool = False, check: bool = False) -> list[str]:
    """Navigate to Coinbase's web page where new coins are announced.

    Args:
        verbose: bool
            Print info about what is found
        check: bool
            Check if the request was successful without errors

    Returns:
        crypto: list[str]
            List of crypto currencies found on coinbase's website
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) "
        + "Gecko/20100101 Firefox/7.0.1"
    }
    try:
        # results = requests.get("https://blog.coinbase.com/", headers=headers)
        results = requests.get("https://blog.coinbase.com/latest", headers=headers)
    except Exception:
        return []
    if check:
        return [str(results.ok)]
    src = results.content
    soup = BeautifulSoup(src, "lxml")
    # main = soup.find_all(
    #     "div",
    #     class_="col u-xs-marginBottom10 u-paddingLeft9 u-paddingRight12 "
    #     + "u-paddingTop0 u-sm-paddingTop20 u-paddingBottom25 "
    #     + "u-size4of12 u-xs-size12of12 u-marginBottom30",
    # )
    # articles = soup.find_all(
    #     "div",
    #     class_="col u-xs-size12of12 js-trackPostPresentation u-paddingLeft12 "
    #     + "u-marginBottom15 u-paddingRight12 u-size4of12",
    # )
    # articles = soup.find_all(
    #     "div",
    #     class_="postArticle-content",
    # )
    articles = soup.find_all(
        "div",
        class_="u-paddingTop20 u-paddingBottom25 u-borderBottomLight js-block",
    )
    crypto = []
    # for item in main:
    #     txt = item.find(
    #         "div",
    #         class_="u-letterSpacingTight u-lineHeightTighter u-breakWord "
    #         + "u-textOverflowEllipsis u-lineClamp4 u-fontSize30 "
    #         + "u-size12of12 u-xs-size12of12 u-xs-fontSize24",
    #     ).text.upper()
    #     the_date = item.find(
    #         "div",
    #         class_="ui-caption u-fontSize12 u-baseColor--textNormal "
    #         + "u-textColorNormal js-postMetaInlineSupplemental",
    #     ).text
    #     crypto = check_coinbase_str(the_date, txt, crypto, verbose)
    for item in articles:
        # txt = item.find(
        #     "div",
        #     class_="u-letterSpacingTight u-lineHeightTighter u-breakWord "
        #     + "u-textOverflowEllipsis u-lineClamp3 u-fontSize24",
        # ).text.upper()
        cls1 = "graf graf--h3 graf-after--figure graf--trailing graf--title"
        cls2 = "graf graf--h3 graf-after--figure graf--title"
        if item.find("h3", class_=cls1) is None:
            if item.find("h3", class_=cls2) is None:
                txt = ""
            else:
                txt = item.find("h3", class_=cls2).text.upper()
        else:
            txt = item.find("h3", class_=cls1).text.upper()
        the_date = item.find(
            "div",
            class_="ui-caption u-fontSize12 u-baseColor--textNormal "
            + "u-textColorNormal js-postMetaInlineSupplemental",
        ).text
        crypto = check_coinbase_str(the_date, txt, crypto, verbose)
    root_logger.info(f"{crypto = }")
    return crypto


def check_coinbase_str(
    dates: str, txt: str, crypto: list[str], verbose: bool
) -> list[str]:
    """Check if the text received from Coinbase includes our special keywords.

    Args:
        dates: the date when the blogpost on Coinbase was written
        txt: the title of the Coinbase blogpost
        crypto: list with new coins found in the Coinbase title
        verbose: whether to print info to stdout or not

    Returns:
        list: list with new coins found in the Coinbase title
    """
    the_date = dates.split()
    # A long, long time ago
    upload_time = datetime.strptime("May 1, 2000", "%b %d, %Y")
    if len(the_date) == 2:
        upload_time = datetime.strptime(
            f"{the_date[0]} {the_date[1]}, 2021", "%b %d, %Y"
        )
        # now = datetime.today() - timedelta(days=20)
    elif len(the_date) == 3:
        upload_time = datetime.strptime(
            f"{the_date[0]} {the_date[1]} {the_date[2]}", "%b %d, %Y"
        )
        # now = datetime.today() - timedelta(days=20)
    recent_enough = datetime.today() - upload_time < timedelta(days=2)
    if "ARE LAUNCHING" in txt and recent_enough:
        for t in txt.split():
            if "(" in t:
                crypto.append(str("".join(re.split("[^a-zA-Z]*", t))))
        if verbose:
            print(f"On {upload_time}:\tCoinbase is listing {crypto}!")
            print(f"{datetime.today() - upload_time} ago")
    return crypto


if __name__ == "__main__":
    res_b = navigate_binance(verbose=True)
    res_c = navigate_coinbase(verbose=True)
    print(res_b)
    print(res_c)
