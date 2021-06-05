import smtplib
import ssl
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from slack_sdk.webhook import WebhookClient

from market_watcher.common import STRATEGIES


class Notifier(object):
    def __init__(self):
        pass

    def notify(self, investment_data):
        raise NotImplementedError

    def _long_straddle_message(self, data):
        sorted_data = {
            ticker: pnl
            for ticker, pnl in sorted(
                data.items(), key=lambda x: abs(x[1]), reverse=True
            )
        }
        formatted_data = self._formatted_data(sorted_data)
        return "\n".join(["Long straddle opportunities:", formatted_data])

    def _short_straddle_message(self, data):
        sorted_data = {
            ticker: pnl
            for ticker, pnl in sorted(
                data.items(), key=lambda x: abs(x[1]), reverse=False
            )
        }
        formatted_data = self._formatted_data(sorted_data)
        return "\n".join(["Short straddle opportunities:", formatted_data])

    def _formatted_data(self, data):
        formatted_data = [
            f"{ticker}: {round(abs(pnl*100),3)}% {self._direction(pnl)}"
            for ticker, pnl in data.items()
        ]
        return "\n".join(formatted_data)

    def _direction(self, number):
        if number > 0:
            return "(UP)"
        elif number < 0:
            return "(DOWN)"
        else:
            return ""


class EmailNotifier(Notifier):
    def __init__(self, config):
        super(EmailNotifier, self).__init__()
        self.__hostname = config["hostname"]
        self.__port = int(config["port"])
        self.__username = config["username"]
        self.__password = config["password"]
        self.__sender = config["sender"]
        self.__recipients = config["recipients"]

    def send(self, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.__hostname, self.__port, context=context) as server:
            if self.__username:
                server.login(self.__username, self.__password)
            server.sendmail(self.__sender, self.__recipients, message)
            print(f"Successfully sent email to {self.__recipients}.")

    def notify(self, investment_data):
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

        long_straddle_message = self._long_straddle_message(
            investment_data[STRATEGIES.LONG_STRADDLE.value]
        )
        short_straddle_message = self._short_straddle_message(
            investment_data[STRATEGIES.SHORT_STRADDLE.value]
        )

        message = MIMEMultipart()
        message["Sender"] = self.__sender
        message["To"] = self.__recipients
        message["Subject"] = f"Investment opportunities report - {current_datetime}"
        text = "\n\n".join([long_straddle_message, short_straddle_message])

        message.attach(MIMEText(text, "plain"))
        self.send(message.as_string())


class SlackNotifier(Notifier):
    def __init__(self, config):
        super(SlackNotifier, self).__init__()
        self.__long_url = config["long url"]
        self.__short_url = config["short url"]

    def notify(self, investment_data):
        long_straddle_message = self._long_straddle_message(
            investment_data[STRATEGIES.LONG_STRADDLE.value]
        )
        short_straddle_message = self._short_straddle_message(
            investment_data[STRATEGIES.SHORT_STRADDLE.value]
        )

        self.send_message(self.__long_url, long_straddle_message)
        self.send_message(self.__short_url, short_straddle_message)

    def send_message(self, url, text):
        """Sends message to Slack channel using webhook."""

        webhook = WebhookClient(url)
        response = webhook.send(text=text)
        assert response.status_code == 200
        assert response.body == "ok"
