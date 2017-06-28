import importlib

class StrategyManager(object):

	def __init__(self):
		return

	def loadStrategy(self, name):
		if name == None:
			return None

		# Load "module.submodule.MyClass"
		strat = getattr(importlib.import_module("app.strategies." + name), name)
		# Instantiate the class (pass arguments to the constructor, if needed)
		return strat
