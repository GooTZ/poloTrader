import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider

class TradingDataProvider(LivetestingDataProvider):

	def __init__(self, APIKey, Secret):
		super().__init__(APIKey, Secret)

	def placeOrder(self, order):
		# TODO: implement actual ordering
		print("placing order: ", order)
