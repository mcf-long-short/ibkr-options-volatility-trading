import time
from enum import Enum

import yaml

from market_watcher.config import context


class STRATEGIES(Enum):
    LONG_STRADDLE = "long straddle"
    SHORT_STRADDLE = "short straddle"


def get_terget_stocks(file_path):
    """Reads target stocks for long/short straddle strategies."""
    try:
        with open(file_path) as f:
            target_stocks = yaml.load(f, Loader=yaml.FullLoader)
            return target_stocks
    except Exception as e:
        print(e)


class MarketWatcherEngine:
    """MarketWatcher core engine logic for scarping financial data."""

    def __init__(self, target_stocks=None):
        self.target_stocks = target_stocks
        self.email_recipient = context.config["EMAIL"]
        self.long_threshlold = float(context.config["LONG_THRESHOLD"])
        self.short_threshlold = float(context.config["SHORT_THRESHOLD"])

    def search_for_intestment_opportunities(self):
        # Update interval for sending email notifications
        update_timeout = int(context.config["UPDATE_TIMEOUT"])

        # Remaining time until email alert
        remaining_seconds = update_timeout

        while context.running:

            if remaining_seconds > 0:
                remaining_seconds -= 1
                time.sleep(1)
            else:
                remaining_seconds = update_timeout
                self.process_latest_market_movements()

    def process_latest_market_movements(self):
        """Goes through each target stock and checks if there is a
        potential invetment opportunity.

        If the opportunity is found trader is notified about it though email
        noticication stating which options trading strategy trader should
        implement.
        """
        for ticker in self.target_stocks:
            strategy = self.target_stocks[ticker]["strategy"]
            daily_pnl = self.get_daily_pnl(ticker)
            # print(ticker, strategy)

            if self.is_investment_opportunity(strategy, daily_pnl):
                self.send_email(ticker, strategy, daily_pnl)

    def get_email_recipient(self):
        """Returns email address to which to send emails to."""
        return self.email_recipient

    def format_email_title(self, ticker, strategy, daily_pnl):
        """Returns formatted email title."""
        return f"{ticker} {daily_pnl}% {strategy}"

    def send_email(self, ticker, strategy, daily_pnl):
        """Send an email notification about potetntial investment opportunity."""
        recipient = self.get_email_recipient()
        title = self.format_email_title(self, ticker, strategy, daily_pnl)

        # TODO: implement logic for sending email (put email config to .env.secret)

    def get_daily_pnl(self, ticker):
        """Returns daily pnl"""
        # TODO: Implement logic for fetching daily pnl for stock
        pass

    def is_investment_opportunity(self, strategy, daily_pnl):
        """Check if the stock is applicable for one of the options trading strategies."""
        if STRATEGIES.LONG_STRADDLE.value == strategy:
            if daily_pnl > self.long_threshlold:
                return True
        elif STRATEGIES.SHORT_STRADDLE.value == strategy:
            if daily_pnl < self.short_threshlold:
                return True

        return False
