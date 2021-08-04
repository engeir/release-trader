"""Schedule run of strategy."""
import time

import schedule

import release_trader.strategy as s


def main() -> None:
    """Release Trader."""
    schedule.every(5).seconds.do(s.buy_on_release)

    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
    # main(prog_name="release-trader")  # pragma: no cover
