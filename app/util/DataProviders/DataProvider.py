import time
import poloniex

from app.util.Error import *

class DataProvider(object):

	polo = None

	registeredFunctions = {}

	timeOfLastTickFetch = time.monotonic()
	timeOfLastCandlestickFetch = time.monotonic()

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
		# TODO: init data from earlier, to give user historic data
		try:
			while True:
				self.doTheLoop()
		except KeyboardInterrupt:
			print("")
			if 'onEnd' in self.registeredFunctions:
				self.registeredFunctions['onEnd']()
			pass

	def doTheLoop(self):
		print("DataProvider.doTheLoop() is not supposed to be called, overwrite it in the used DataProvider!")
		exit(2)
