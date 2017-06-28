import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider
import app.util.Timing

class LivetestingDataProvider(DataProvider):

	candle = {}

	def __init__(self, APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue):
		super().__init__(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)

	def doTheLoop(self):
		# Once a second print the fetching-data string
		timeofThisLoop = time.monotonic()
		delta = self.timeOfLastOrder - timeofThisLoop
		if delta > -1:
			return # next iteration if not enough time passed
		self.timOfLastOrder = timeofThisLoop
		print("Fetching data " + self.getSpinner(), end = "\r")

		tickerData = self.getTickerData("BTC_ETH")
		t = int(time.time())
		self.appendToCandle(t, tickerData)

		if not (self.orderQueue.empty()):
			order = self.orderQueue.get()
			self.placeOrder(order)

		deltaMinute = self.timeOfLastTickFetch - timeofThisLoop
		if deltaMinute > -60:
			return # next iteration if not enough time passed
		self.timeOfLastTickFetch = timeofThisLoop

		self.appendCandleToData("BTC_ETH", self.candle)
		self.candle.clear()

	def appendCandleToData(self, pair, candle):
		dataDict = {'date': candle['date'], 'low': candle['low'], 'open': candle['open'], 'average': candle['average'] / self.secondsPassed,
		'close': candle['close'], 'high': candle['high'], 'volume': candle['volume'] / self.secondsPassed, 'isFrozen': candle['isFrozen']}
		self.dataQueue.put(("Current", dataDict))
		self.secondsPassed = 0


	def getTickerData(self, pair):
		tickerData = self.polo.returnTicker()
		return tickerData[pair]

	"""
	The base function for placing an order on poloniex. Will be overriden by some DataProviders. Otherwise just prints the placed order.

	@param order: A tuple with order informations
	@return: None
	"""
	def placeOrder(self, order):
		super().placeOrder(order)
		balances = self.polo.returnBalances()
		self.dataQueue.put(("Balances", balances))
