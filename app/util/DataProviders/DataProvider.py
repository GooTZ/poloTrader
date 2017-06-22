import time
import poloniex
from collections import deque

from app.util.Error import *
from app.util.Timing import TimePeriod

class DataProvider(object):

	polo = None

	registeredFunctions = {}

	timeOfLastTickFetch = time.monotonic()
	timeOfLastCandlestickFetch = time.monotonic()
	timOfLastOrder = time.monotonic()

	timePeriod = TimePeriod.T300
	orderQueue = deque()

	def __init__(self, APIKey, Secret):
		self.polo = poloniex.Poloniex(APIKey, Secret)

	def registerStrategy(self, strat):
		for func in strat.getRegisteredFunctions():
			if not func == None:
				self.registeredFunctions[func.__name__] = func

		if not ('initialize' in self.registeredFunctions):
			raise FunctionNotFoundError('initialize', "Function could not be found")
		if not ('onData' in self.registeredFunctions):
			raise FunctionNotFoundError('onData', "Function could not be found")

	def enterDataLoop(self):
		self.registeredFunctions['initialize']()
		timeOfLastTickFetch = time.monotonic()
		timeOfLastCandlestickFetch = time.monotonic()

		try:
			while True:
				self.doTheLoop()
		except KeyboardInterrupt:
			print("")
			if 'onEnd' in self.registeredFunctions:
				self.registeredFunctions['onEnd']()
			pass

	def doTheLoop(self):
		pass

	def setTimePeriod(timePeriod):
		# TODO: check if timePeriod is TimePeriod, log warning if not
		self.timePeriod = timePeriod

	def placeOrder(self, order):
		print("placing order: ", order)
