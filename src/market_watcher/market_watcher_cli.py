import yaml
import click
from click.utils import echo

from market_watcher.version import VERSION
from market_watcher.config import config


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
def test_send_mail():
    email = config["EMAIL"]
    echo(f"Email notifications are sent to: {email}")


@cli.command()
@click.option(
    "--stocks",
    default=r"src/market_watcher/research/target_stocks.yaml",
    help="Yaml file containing target stocks for long and short straddle option strategy..",
)
def start(stocks):
    """Starts the MarketWatcher."""
    echo(f"Reading terget stocks from file: {stocks}")

    with open(stocks) as file:
        target_stocks = yaml.load(file, Loader=yaml.FullLoader)

        print(target_stocks)


@cli.command()
def stop():
    """Stops the MarketWatcher."""
    echo(f"Stopping MarketWatcher...")
