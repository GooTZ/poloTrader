import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider
import app.util.Timing

class LivetestingDataProvider(DataProvider):

	def __init__(self, APIKey, Secret):
		super().__init__(APIKey, Secret)

	def doTheLoop(self):
		# Place one order per second
		# # limit the calls to once a minute
		timeofThisLoop = time.monotonic()
		delta = self.timeOfLastOrder - timeofThisLoop
		if delta > -1:
			return # next iteration if not enough time passed
		self.timOfLastOrder = timeofThisLoop
		self.placeOrder(orderQueue.popleft())

		# limit the calls to once a minute
		deltaMinute = self.timeOfLastTickFetch - timeofThisLoop
		if deltaMinute > -(1 * 60):
			return # next iteration if not enough time passed
		self.timeOfLastTickFetch = timeofThisLoop

		# TODO: api calls take pretty long, better timing maybe?
		# Fetch all fast pased data from poloniex
		ticker = self.polo.returnTicker()
		orderbook = self.polo.returnOrderBook()
		#self.polo.returnTradeHistory()
		self.registeredFunctions['onData']()

		if 'getOrderQueue' in self.registeredFunctions:
			orderQueue = self.registeredFunctions['getOrderQueue']()

		localtime = time.asctime( time.localtime(time.time()) )
		print(localtime)

		# execute this part of the loop only once every n minutes
		# where n is the specified self.timePeriod
		delta5Min = self.timeOfLastCandlestickFetch - timeofThisLoop
		if delta5Min > self.timePeriod:
			return # next iteration if not enough time passed
		self.timeOfLastCandlestickFetch = timeofThisLoop

		# TODO: fetch for every pair or only specified ones?
		# TODO: start = unixTimestamp(self.timeOfLastCandlestickFetch)
		start = app.util.Timing.getHistoricTimestamp(minute = self.timePeriod)
		chart = self.polo.returnChartData("BTC_ETH", period = self.timePeriod, start = start, end = 9999999999)
		print(chart)
