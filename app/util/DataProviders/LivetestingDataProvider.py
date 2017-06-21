import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider

class LivetestingDataProvider(DataProvider):

	def __init__(self, APIKey, Secret):
		super().__init__(APIKey, Secret)

	def doTheLoop(self):
		# limit the calls to once a minute
		timeofThisLoop = time.monotonic()
		delta1 = self.timeOfLastTickFetch - timeofThisLoop
		if delta1 > -1:
			return # next iteration if not enough time passed
		self.timeOfLastTickFetch = timeofThisLoop

		# TODO: api calls take pretty long, better timing maybe?
		# Fetch all fast pased data from poloniex
		self.polo.returnTicker()
		self.polo.returnOrderBook()
		#self.polo.returnTradeHistory()
		self.registeredFunctions['onData']()

		#
		orderQ = list()
		if 'getOrderQueue' in self.registeredFunctions:
			orderQ = self.registeredFunctions['getOrderQueue']()
		for order in orderQ:
			# TODO: get order infos and pass to function
			placeOrder()

		localtime = time.asctime( time.localtime(time.time()) )
		print(localtime)

		# execute this part of the loop only once every 5 minutes
		# TODO: call only every specified tick
		delta1 = self.timeOfLastCandlestickFetch - timeofThisLoop
		if delta1 > -4.5:
			return # next iteration if not enough time passed
		self.timeOfLastCandlestickFetch = timeofThisLoop

		# TODO: fetch for every pair or only specified ones?
		# TODO: start = unixTimestamp(self.timeOfLastCandlestickFetch)
		# TODO: set specified tick
		#self.polo.returnChartData(self.pair, period = 300, start = start, end = 9999999999)

	def placeOrder(self):
		print("placing order")
