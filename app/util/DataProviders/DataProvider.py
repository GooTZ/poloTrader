class DataProvider(object):

	APIKey = ''
	Secret = ''

	registeredFunctions = list()

	def __init__(self, APIKey, Secret):
		self.APIKey = APIKey
		self.Secret = Secret

	def registerStrategy(self, strat):
		self.registeredFunctions = strat.getRegisteredFunctions()
		for func in strat.getRegisteredFunctions():
			if not func == None:
				func()

	def enterDataLoop(self):
		print("TODO: implement DataProvider.enterDataLoop()")
