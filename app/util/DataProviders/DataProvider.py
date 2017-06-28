import time
import poloniex
import datetime
from collections import deque
from threading import Thread

from app.util.Error import *
from app.util.Timing import TimePeriod

class DataProvider(Thread):

	DATA_DIR = ""

	polo = None

	# Thread-shared orderQueue
	orderQueue = None
	# Thread-shared instructionQueue
	instructionQueue = None
	# Thread-shared dataQueue
	dataQueue = None

	registeredFunctions = {}

	timeOfLastTickFetch = time.monotonic()
	timeOfLastCandlestickFetch = time.monotonic()
	timeOfLastOrder = time.monotonic()

	timePeriod = TimePeriod.T300

	dataFrame = None

	secondsPassed = 0

	def __init__(self, APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue):
		self.polo = poloniex.Poloniex(APIKey, Secret)

		self.dataQueue = dataQueue
		self.orderQueue = orderQueue
		self.instructionQueue = instructionQueue

		self.DATA_DIR = dataDir

		Thread.__init__(self)
		self.daemon = True

	def run(self):
		self.enterDataLoop()

	"""
	Sets the connection between the chosen strategy and the dataprovider up.

	@param strat: The chosen strategy
	@return: None.
	"""
	def registerStrategy(self, strat):
		for func in strat.getRegisteredFunctions():
			if not func == None:
				self.registeredFunctions[func.__name__] = func

		self.dataFrame = strat.getData()

		if not ('initialize' in self.registeredFunctions):
			raise FunctionNotFoundError('initialize', "Function could not be found")
		if not ('onData' in self.registeredFunctions):
			raise FunctionNotFoundError('onData', "Function could not be found")

	"""
	Beginns the infinite loop which pulls and processes data.

	@return: None.
	"""
	def enterDataLoop(self):
		#self.registeredFunctions['initialize']()
		self.timeOfLastTickFetch = time.monotonic()
		self.timeOfLastCandlestickFetch = time.monotonic()

		while True:
			self.doTheLoop()


	"""
	A function stub, used so the DataProvider class, does nothing. Other DataProvider classes must overwrite this function

	@return: None.
	"""
	def doTheLoop(self):
		pass

	# TODO: what is this supposed to do?
	def setTimePeriod(timePeriod):
		# TODO: check if timePeriod is TimePeriod, log warning if not
		self.timePeriod = timePeriod

	"""
	The base function for placing an order on poloniex. Will be overriden by some DataProviders. Otherwise just prints the placed order.

	@param order: A tuple with order informations
	@return: None
	"""
	def placeOrder(self, order):
		t = datetime.datetime.utcnow()
		print(t, "placing order: ", str(order))

	"""
	A helper function that prints a semi-rotating bar to show progress.

	@return: None.
	"""
	def getSpinner(self):
		t = int(time.time())
		dt = t - (int(t / 10) * 10)
		if ((dt % 2) == 0):
			return "─"
		return "|"

	"""
	Updates the current candlestick with new data. Used by DataProviders that use live data.

	@param time: The epoch timestamp of the data.
	@param data: A dict of the latest ticker data.
	@return: None.
	"""
	def appendToCandle(self, time, data):
		self.candle['date'] = time

		if not 'low' in self.candle:
			self.candle['low'] = float(data['last'])
		elif float(data['lowestAsk']) < self.candle['low']:
			self.candle['low'] = float(data['lowestAsk'])

		if not 'open' in self.candle:
			self.candle['open'] = float(data['last'])

		if not 'average' in self.candle:
			self.candle['average'] = float(data['last'])
		else:
			self.candle['average'] += float(data['last'])

		self.candle['close'] = data['last']

		if not 'high' in self.candle:
			self.candle['high'] = float(data['last'])
		elif float(data['highestBid']) > self.candle['high']:
			self.candle['high'] = float(data['highestBid'])

		if not 'volume' in self.candle:
			self.candle['volume'] = float(data['baseVolume'])
		else:
			self.candle['volume'] += float(data['baseVolume'])

		if data['isFrozen'] == "1":
			self.candle['isFrozen'] = True
		else:
			self.candle['isFrozen'] = False

		self.secondsPassed += 1
