# poloTrader
My personal Poloniex altcoin trader. Heavily inspired by quantopian.

## How to use

### Installation

To clone and run this application, you'll need [Git](https://git-scm.com/) and [Python 3](https://www.python.org/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/GooTZ/poloTrader.git

# Go into the repository
$ cd poloTrader

# Install dependencies
$ python setup.py
```

### Configuration

In order to use the trading capabilities you first have to set up the script to use your Poloniex APIKey and Secret.

`cp example-config.yaml config.yaml`

Edit the `config.yaml` and enter your APIKey and Secret.

### Usage

The script can be executed in the following manner:

`python run.py -m <mode>`

with the following modes availible:

`TESTING`: Fetches data from csv files. Used for backtesting your algorithm.

`LIVE_TESTING`: Gets the live data from Poloniex, but does not perform actual trading actions.

`TRADING`: Trades live on Poloniex according to your algorithm. Use on your own risk!

`FETCH_DATA`: Fetches live data and saves it in csv files to use it for future backtesting.

## Writing your own Algorithm

This section is still work in progress.

## Credits
This software uses several open source packages.

* [Python 3](https://www.python.org/)
* [python-poloniex](https://github.com/s4w3d0ff/python-poloniex)

Also special thanks to:
* [Poloniex](https://poloniex.com/) for providing the trading platform and API.
* [Quantopian](https://www.quantopian.com/) for the great inspiration in the scripting environment.
