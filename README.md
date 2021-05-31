# Interactive Brokers: Volatility trading with options

## Introduction

`Volatility trading` using `equity options` and `long/short straddle` option strategies combined with a `momentum strategy` to profit from a high/low daily volatility in US equities.

We are using Interactive Brokers Trader Workstation paper trading account to test our trading stategy. For day trading sessions we implemented simple trading bot to quickly react on the market moves ([Python TWS API](https://tradersacademy.online/trading-courses/python-tws-api)).

This repository represents group project work for implementing option trading strategies (course in Financial Derivatives for advanced degree [Masters in Computational Finance, Union University](http://mcf.raf.edu.rs/)).

## Results

Final P&L overview after one week of trading.

## Trading strategy

Trading strategy is based on `volatility trading`. We do day trading, getting in and out of the positions in the same trading session.

In order to profit on a high or low volatility in the equities we trade with options using `long straddle` and `short stradle` strategy respectively. For intuition about these strategies we highly recommend watching following videos:

- [Long Straddle](https://www.youtube.com/watch?v=4UlIMmXhjsc)
- [Short Straddle](https://www.youtube.com/watch?v=Lsk9ppb8ffs)

We first begin with doing basic market research and finding historically the most and least volatile stocks in the past 2 week, 4 week and 2 month period in the `Russel 3000 index` (in order to capture both the large-cap and the small-cap companies). Using naive expecation for the future volatility based on the historical volatility combined with the momentum on a daily level for the target companies, we enter into `long straddle` or `short straddle` positions.

### Order type

Stop loss/ Bracket order

## How to use MarketWatcher trading bot?

Based on cofigured environment variables in .env file (`email notification interval time` and `daily P&L threashold values` for both strategies) and provided .yaml file with `target stocks (ticker and long/short straddle strategy indicator for that ticker)`, MarketWatcher engine listens to real-time ticker data feed and notifies us when there is a `potential opportunity for entering into long or short straddle options position`, with that stock as an underlying.

You can control MarketWatcher trading bot using simple command-line-tool we built. And after bot is started it will send us an email for each investment opportunity it finds for our target stocks.

CLI commands:

```bash
market_watcher_cli start
market_watcher_cli stop
market_watcher_cli email-config
```

Example ClI output upon starting MarketWatcher engine:

```
         ______              _              _  _  _                 _
        |  ___ \            | |         _  | || || |      _        | |
        | | _ | | ____  ____| |  _ ____| |_| || || | ____| |_  ____| | _   ____  ____
        | || || |/ _  |/ ___) | / ) _  )  _) ||_|| |/ _  |  _)/ ___) || \ / _  )/ ___)
        | || || ( ( | | |   | |< ( (/ /| |_| |___| ( ( | | |_( (___| | | ( (/ /| |
        |_||_||_|\_||_|_|   |_| \_)____)\___)______|\_||_|\___)____)_| |_|\____)_|

        MarketWatcher tool for finding investiments opportunities on Interacive Brokers
        for volatility trading on equity market using long and short options strategy.

        version: v0.1.0




        Starting MarketWatcher...
        MarketWatcher started.
```

You can run cli tool from:

- Docker container (using docker-compose)
- Python virtual environment

### 1. Running in Docker

Building docker image:

```bash
docker build -t my_image --rm .
```

Running docker-compose:

```bash
docker-compose run --rm app
```

After docker-compose command you can run any on the cli commands:

```bash
market_watcher_cli --help
market_watcher_cli start
market_watcher_cli stop
market_watcher_cli email-config
```

### 2. Running in virtual environment

Install virtual environment for python 3.x:

```bash
python3 -m venv /path/to/new/virtual/environment
```

Activate environment:

```bash
source .venv/bin/activate
```

To check if everything installed well:

```bash
which python
which pip
pip lists
```

Install requirements:

```bash
pip install -r requirements.txt
```

Install `ibapi` client (so you can use `import ibapi` in the code for this python venv):

```bash
cd src/market_watcher/ib_client
python setup.py bdist_wheel
pip install src/ib_client/dist/ibapi-9.76.1-py3-none-any.whl
```

To check if `ibapi` was successfully installed run tests:

```bash
python -m unittest discover -s src/ib_client/tests
```

### Installing MarketWatcher trading bot:

```bash
cd src
pip install --editable .
```

## IBKR: Implementing market data scanner trading bot

### IBKR requirements

Requirements for enabling [Trader Workstation API](https://interactivebrokers.github.io/tws-api/):

- Download and install [Trader Workstation](https://www.interactivebrokers.com/en/index.php?f=14099#tws-software)
- Download and install [IB Gateway](https://www.interactivebrokers.com/en/index.php?f=16457)
- Enable following setting in the TWS (`File -> Global Configuration -> API -> Settings`):
  1. Enable ActiveX and Socket Clients
  2. Read-Only API (no order placing, only data reading for our scraping bot)
  3. Socket port: 7497 (Paper)/7496(Live)
  4. Allow connections from localhost only
  5. Create API message log file
  6. Logging Level: Error
- Download [TWS API source code](https://interactivebrokers.github.io/#)
