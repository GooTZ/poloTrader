import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider

class TradingDataProvider(LivetestingDataProvider):

	def __init__(self, APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue):
		super().__init__(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)

	def placeOrder(self, order):
		# TODO: implement actual ordering
		print("placing order: ", order)
