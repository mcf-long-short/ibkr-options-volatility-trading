import time
from enum import Enum

import yaml

from yahoofinancials import YahooFinancials

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

def get_email_config():
    email_config = {}
    email_config['hostname'] = context.config["SMTP_HOSTNAME"]
    email_config['port'] = context.config["SMTP_PORT"]
    email_config['username'] = context.config["SMTP_USERNAME"]
    email_config['password'] = context.config["SMTP_PASSWORD"]
    email_config['sender'] = context.config["EMAIL_SENDER"]
    email_config['recipients'] = context.config["EMAIL_RECIPIENTS"]
    return email_config

def get_slack_config():
    slack_config = {}
    slack_config['long url'] = context.config["SLACK_LONG_WEBHOOK"]
    slack_config['short url'] = context.config["SLACK_SHORT_WEBHOOK"]
    return slack_config


class MarketWatcherEngine:
    """MarketWatcher core engine logic for scarping financial data."""

    def __init__(self, target_stocks=None, notifier=None):
        self.target_stocks = target_stocks
        self.notifier = notifier

        self.long_threshlold = float(context.config["LONG_THRESHOLD"])
        self.short_threshlold = float(context.config["SHORT_THRESHOLD"])

        self.daily_pnls = self.get_daily_pnls()

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
        investment_opportunities = []
        for ticker in self.target_stocks:
            if self.is_investment_opportunity(self.target_stocks[ticker]["strategy"], abs(self.daily_pnls[ticker])):
                investment_opportunities.append(ticker)

        investment_data = self.get_investment_data(investment_opportunities)

        self.notifier.notify(investment_data)

    def get_daily_pnls(self):
        """Returns daily pnls"""
        target_stocks = list(self.target_stocks.keys())
        yahoo_financials_target_stocks = YahooFinancials(target_stocks)
        return yahoo_financials_target_stocks.get_current_percent_change()

    def get_investment_data(self, investment_opportunities):
        """Returns two dictionaries that contain investment data for both strategies"""
        long_straddle = {}
        short_straddle = {}

        for ticker in investment_opportunities:
            if STRATEGIES.LONG_STRADDLE.value == self.target_stocks[ticker]["strategy"]:
                long_straddle[ticker] = self.daily_pnls[ticker]
            elif STRATEGIES.SHORT_STRADDLE.value == self.target_stocks[ticker]["strategy"]:
                short_straddle[ticker] = self.daily_pnls[ticker]

        return {STRATEGIES.LONG_STRADDLE.value: long_straddle, STRATEGIES.SHORT_STRADDLE.value: short_straddle}

    def is_investment_opportunity(self, strategy, abs_daily_pnl):
        """Check if the stock is applicable for one of the options trading strategies."""
        if STRATEGIES.LONG_STRADDLE.value == strategy:
            if abs_daily_pnl > self.long_threshlold:
                return True
        elif STRATEGIES.SHORT_STRADDLE.value == strategy:
            if abs_daily_pnl < self.short_threshlold:
                return True

        return False
