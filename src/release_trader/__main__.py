"""Command-line interface."""
import release_trader.trade as trd


def main() -> None:
    """Release Trader."""
    trd.buy_crypto()


if __name__ == "__main__":
    main()
    # main(prog_name="release-trader")  # pragma: no cover
