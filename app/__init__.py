import yaml
from app.strategies.MovingAverages import MovingAverages
from app.strategies.BaseStrategy import BaseStrategy
from app.util.TradingMode import TradingMode
from app.util.DataProviders.DataProvider import DataProvider
from app.util.DataProviders.TestingDataProvider import TestingDataProvider

def run(mode):
	# read the config
	with open('config.yaml', 'r') as f:
		doc = yaml.load(f)

	# get the api key and secret
	APIKey = doc["api"]["key"]
	Secret = doc["api"]["secret"]

	# check which mode we are trading in
	# instantiate a corresponding data provider
	dataProvider = None
	if (mode == TradingMode.TESTING):
		dataProvider = TestingDataProvider(APIKey, Secret)
	elif (mode == TradingMode.LIVE_TESTING):
		dataProvider = LivetestingDataProvider(APIKey, Secret)
	elif (mode == TradingMode.TRADING):
		#dataProvider = TradingDataProvider(APIKey, Secret)
		print("TODO: Implement this")
		exit(2)

	# TODO: write a strategy manager
	# check which strategy we are using
	# instantiate the chosen strategy
	#
	# Currently only instantiates the sample strategy
	strategy = MovingAverages()

	# TODO
	# register the strategy to the data provider
	dataProvider.registerStrategy(strategy)

	# TODO
	# enter the data loop
	dataProvider.enterDataLoop()

	exit()
