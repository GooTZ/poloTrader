import yaml
import os.path
import logging

from app.strategies.MovingAverages import MovingAverages
from app.strategies.BaseStrategy import BaseStrategy
from app.util.TradingMode import TradingMode
from app.util.DataProviders.DataProvider import DataProvider
from app.util.DataProviders.TestingDataProvider import TestingDataProvider
from app.util.DataProviders.LivetestingDataProvider import LivetestingDataProvider
from app.util.StrategyManager import StrategyManager
from app.util.Error import *

def run(mode, strategyName = None):
	# check if config file exists
	if not os.path.isfile('config.yaml'):
		raise FileNotFoundError("File 'config.yaml' not found!")
	# read the config
	with open('config.yaml', 'r') as f:
		doc = yaml.load(f)

	# check if api key and secret exist in the config
	if not (("api" in doc) or ("key" in doc["api"]) or ("secret" in doc["api"])):
		error = "Poloniex APIKey and Secret are not properly configured in 'config.yaml'!"
		raise ConfigError(error)

	# get the api key and secret
	APIKey = doc["api"]["key"]
	Secret = doc["api"]["secret"]

	if strategyName == None:
		if not ("strategy" in doc):
			error = "No strategy specified in neither the command or in 'config.yaml'!"
			raise ConfigError(error)
		else:
			strategyName = doc["strategy"]

	# check which mode we are trading in
	# instantiate a corresponding data provider
	dataProvider = None
	if (mode == TradingMode.TESTING):
		dataProvider = TestingDataProvider(APIKey, Secret)
	elif (mode == TradingMode.LIVE_TESTING):
		dataProvider = LivetestingDataProvider(APIKey, Secret)
	elif (mode == TradingMode.TRADING):
		dataProvider = TradingDataProvider(APIKey, Secret)
	elif (mode == TradingMode.FETCH_DATA):
		dataProvider = HistoryDataProvider(APIKey, Secret)
	else:
		raise UnsupportedModeError(mode, "The given mode is not supported!")


	# Get the configured Strategy and instantiate it
	strategyManager = StrategyManager()
	strategy = strategyManager.loadStrategy(strategyName)

	# register the strategy to the data provider
	dataProvider.registerStrategy(strategy)

	# enter the data loop
	dataProvider.enterDataLoop()

	exit()
