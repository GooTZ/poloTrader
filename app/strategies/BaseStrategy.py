class BaseStrategy(object):

	registeredFunctions = list()

	def __init__(self):
		print("BaseStrategy instantiated!")
		self.registerFunction(self.onData)
		self.registerFunction(self.initialize)

	"""
	Called once at the start of the algorithm.
	"""
	def initialize(self):
		print("BaseStrategy: initialize()")

	"""
	Called every configured tick.
	"""
	def onData(self):
		print("BaseStrategy: onData()")

	"""
	Returns all registered functions to be called by the data provider
	"""
	def getRegisteredFunctions(self):
		return self.registeredFunctions

	"""
	Registers the function func for the data provider
	"""
	def registerFunction(self, func):
		self.registeredFunctions.append(func)
