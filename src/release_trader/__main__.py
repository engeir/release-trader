"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Release Trader."""


if __name__ == "__main__":
    main(prog_name="release-trader")  # pragma: no cover
