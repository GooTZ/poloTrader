from app.strategies.BaseStrategy import BaseStrategy

class MovingAverages(BaseStrategy):

	def __init__(self):
		print("MovingAverages instantiated!")
		super().__init__()
		self.registerFunction(self.onEnd)

	"""
	Called once at the start of the algorithm.
	"""
	def initialize(self):
		print("MovingAverages: initialize()")

	"""
	Called every configured tick.
	"""
	def onData(self):
		print("MovingAverages.onData() -> ", self.data.historic("BTC_ETH", "open", 1, 300))

	"""
	Called when the loop ends
	"""
	def onEnd(self):
		print(self.context)
		print("The loop just ended!")
