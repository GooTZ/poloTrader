from app.strategies.BaseStrategy import BaseStrategy

class MovingAverages(BaseStrategy):

	def __init__(self):
		print("MovingAverages instantiated!")
		super().__init__()

	"""
	Called once at the start of the algorithm.
	"""
	def initialize(self):
		print("MovingAverages: initialize()")

	"""
	Called every configured tick.
	"""
	def onData(self):
		print("MovingAverages: onData()")
