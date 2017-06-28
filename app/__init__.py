import toml
import os.path
import logging

from queue import LifoQueue as Queue

from app.strategies.MovingAverages import MovingAverages
from app.strategies.BaseStrategy import BaseStrategy
from app.util.TradingMode import TradingMode
from app.util.DataProviders.DataProvider import DataProvider
from app.util.DataProviders.TestingDataProvider import TestingDataProvider
from app.util.DataProviders.LivetestingDataProvider import LivetestingDataProvider
from app.util.DataProviders.HistoryDataProvider import HistoryDataProvider
from app.util.StrategyManager import StrategyManager
from app.util.Error import *

def run(mode, strategyName = None):
	# check if config file exists
	if not os.path.isfile('config.toml'):
		raise FileNotFoundError("File 'config.toml' not found!")
	# read the config
	with open("config.toml") as conffile:
		config = toml.loads(conffile.read())

	# check if api key and secret exist in the config
	if not (("api" in config) or ("key" in config["api"]) or ("secret" in config["api"])):
		error = "Poloniex APIKey and Secret are not properly configured in 'config.toml'!"
		raise ConfigError(error)

	# get the api key and secret
	APIKey = config["api"]["key"]
	Secret = config["api"]["secret"]
	# get the data directory from the config
	dataDir = config["misc"]["dataDirectory"]

	if strategyName == None:
		if not ("strategy" in config["misc"]):
			error = "No strategy specified in neither the command or in 'config.toml'!"
			raise ConfigError(error)
		else:
			strategyName = config["misc"]["strategy"]

	# Shared Variables between the threads
	dataQueue = Queue()
	orderQueue = Queue()
	instructionQueue = Queue()

	# check which mode we are trading in
	# instantiate a corresponding data provider
	dataProvider = None
	if (mode == TradingMode.TESTING):
		dataProvider = TestingDataProvider(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)
	elif (mode == TradingMode.LIVE_TESTING):
		dataProvider = LivetestingDataProvider(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)
	elif (mode == TradingMode.TRADING):
		dataProvider = TradingDataProvider(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)
	elif (mode == TradingMode.FETCH_DATA):
		dataProvider = HistoryDataProvider(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)
	else:
		raise UnsupportedModeError(mode, "The given mode is not supported!")

	# Get the configured Strategy and instantiate it
	strategyManager = StrategyManager()
	strategy = strategyManager.loadStrategy(strategyName)(dataQueue, orderQueue)

	# Start both threads
	dataProvider.start()
	strategy.start()

	# Enter Infinite loop until the user breaks it
	try:
		while True:
			continue
	except KeyboardInterrupt:
		print("")
		pass

	exit()
