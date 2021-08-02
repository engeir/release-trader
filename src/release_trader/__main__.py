"""Command-line interface."""
# from threading import Timer
import time

import schedule

import release_trader.strategy as s

# import release_trader.trade as trd


def main() -> None:
    """Release Trader."""
    # s.buy_on_release()

    # Timer(5, main).start()
    schedule.every(5).seconds.do(s.buy_on_release)

    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
    # main(prog_name="release-trader")  # pragma: no cover
