import click
from click.utils import echo

from market_watcher.version import VERSION
from market_watcher.config import context
from market_watcher.common import get_terget_stocks
from market_watcher.common import MarketWatcherEngine


@click.group()
def cli():
    """MarketWatcher cli commands."""
    echo(
        """
         ______              _              _  _  _                 _                 
        |  ___ \            | |         _  | || || |      _        | |                
        | | _ | | ____  ____| |  _ ____| |_| || || | ____| |_  ____| | _   ____  ____ 
        | || || |/ _  |/ ___) | / ) _  )  _) ||_|| |/ _  |  _)/ ___) || \ / _  )/ ___)
        | || || ( ( | | |   | |< ( (/ /| |_| |___| ( ( | | |_( (___| | | ( (/ /| |    
        |_||_||_|\_||_|_|   |_| \_)____)\___)______|\_||_|\___)____)_| |_|\____)_|    
                                                                                                             
        MarketWatcher tool for finding investiments opportunities on Interacive Brokers
        for volatility trading on equity market using long and short options strategy.
    """
    )
    echo(f"version: v{VERSION}")
    echo("\n\n\n")


@cli.command()
def email_config():
    """Lists email recipient and email title format."""
    market_watcher_engine = MarketWatcherEngine()

    email = market_watcher_engine.get_email_recipient()
    title = market_watcher_engine.format_email_title(
        ticker="MSFT", strategy="Long Straddle", daily_pnl="-5.2"
    )

    echo(f"Email notifications are sent to: {email}")
    echo(f"Email Title format: {title}")


@cli.command()
@click.option(
    "--stocks",
    default=r"src/market_watcher/research/target_stocks.yaml",
    help="Yaml file containing target stocks for long and short straddle option strategy..",
)
def start(stocks):
    """Starts the MarketWatcher."""
    echo(f"Starting MarketWatcher...")

    try:
        context.running = True
        echo(f"MarketWatcher started.")

        echo(f"Reading terget stocks from file: {stocks}")
        target_stocks = get_terget_stocks(stocks)

        market_watcher_engine = MarketWatcherEngine(target_stocks=target_stocks)
        market_watcher_engine.search_for_intestment_opportunities()
    except ValueError as e:
        echo(e)


@cli.command()
def stop():
    """Stops the MarketWatcher."""
    echo(f"Stopping MarketWatcher...")

    try:
        context.running = False
        echo(f"MarketWatcher stopped.")
    except ValueError as e:
        echo(e)
