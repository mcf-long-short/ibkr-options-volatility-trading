import click
from click.utils import echo

from market_watcher.version import VERSION
from market_watcher.config import context
from market_watcher.common import get_terget_stocks
from market_watcher.common import get_email_config, get_slack_config
from market_watcher.common import MarketWatcherEngine
from market_watcher.notifier import EmailNotifier, SlackNotifier


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
def test_slack():
    """Sends dummy messages to test if Slack app has been configured properly."""

    try:
        echo("Testing Slack options-trading bot...")

        config = get_slack_config()
        slack_notifier = SlackNotifier(config)

        echo("Sending message to #options-long-straddle channel...")
        slack_notifier.send_message(config["long url"], "MarketWatcher: Test long!")

        echo("Sending message to #options-short-straddle channel...")
        slack_notifier.send_message(config["short url"], "MarketWatcher: Test short!")
    except Exception as e:
        echo("Slack testing failed!")
        echo(e)


@cli.command()
@click.option(
    "--notifier",
    default="all",
    help="Available options: email, slack, all",
)
def config(notifier):
    """Lists congiguration for slack and email notifiers."""

    if notifier == "all" or notifier == "slack":
        config = get_slack_config()
        for env in config:
            echo(f"{env}: {config[env]}")

    if notifier == "all" or notifier == "email":
        config = get_email_config()
        for env in config:
            echo(f"{env}: {config[env]}")


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

        echo(f"Reading target stocks from file: {stocks}")
        target_stocks = get_terget_stocks(stocks)

        notifiers = []

        if context.state["email"]:
            echo("Instantiating email notifier.")
            notifiers.append(EmailNotifier(get_email_config()))

        if context.state["slack"]:
            echo("Instantiating slack notifier.")
            notifiers.append(SlackNotifier(get_slack_config()))

        echo("Instantiating MarketWatcher and running the engine.")
        market_watcher_engine = MarketWatcherEngine(
            target_stocks=target_stocks, notifiers=notifiers
        )
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
