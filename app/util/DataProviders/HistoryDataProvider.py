import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider

class HistoryDataProvider(DataProvider):

	def __init__(self, APIKey, Secret):
		super().__init__(APIKey, Secret)
