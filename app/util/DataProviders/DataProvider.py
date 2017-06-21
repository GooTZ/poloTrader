import time
import poloniex

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

		# TODO: rework errors
		if not ('initialize' in self.registeredFunctions):
			print("ERROR: No initialize function got registered in the TradingStrategy!")
			exit(2)
		if not ('onData' in self.registeredFunctions):
			print("ERROR: No onData function got registered in the TradingStrategy!")
			exit(2)

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
		# TODO: better message
		print("Not supposed to be called!")
		exit(2)
