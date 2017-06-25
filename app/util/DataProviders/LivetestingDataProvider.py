import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider
import app.util.Timing

class LivetestingDataProvider(DataProvider):

	candle = {}
	c = 0

	def __init__(self, APIKey, Secret):
		super().__init__(APIKey, Secret)

	def doTheLoop(self):
		# Once a second print the wip string
		timeofThisLoop = time.monotonic()
		delta = self.timeOfLastOrder - timeofThisLoop
		if delta > -1:
			return # next iteration if not enough time passed
		self.timOfLastOrder = timeofThisLoop
		print("Fetching data " + self.getSpinner(), end = "\r")

		tickerData = self.getTickerData("BTC_ETH")
		t = int(time.time())
		self.appendToCandle(t, tickerData)

		if (len(self.orderQueue) > 0):
			order = self.orderQueue.popleft()
			self.placeOrder(order)

		deltaMinute = self.timeOfLastTickFetch - timeofThisLoop
		if deltaMinute > -60:
			return # next iteration if not enough time passed
		self.timeOfLastTickFetch = timeofThisLoop

		self.appendCandleToData("BTC_ETH", self.candle)
		self.candle.clear()

		self.registeredFunctions['onData']()

		if 'getOrderQueue' in self.registeredFunctions:
			self.orderQueue = self.registeredFunctions['getOrderQueue']()

	def appendCandleToData(self, pair, candle):
		dataDict = {'date': candle['date'], 'low': candle['low'], 'open': candle['open'], 'average': candle['average'] / self.c,
		'close': candle['close'], 'high': candle['high'], 'volume': candle['volume'] / self.c, 'isFrozen': candle['isFrozen']}
		self.dataFrame.updateCurrent(pair, dataDict)
		self.c = 0


	def getTickerData(self, pair):
		tickerData = self.polo.returnTicker()
		return tickerData[pair]
