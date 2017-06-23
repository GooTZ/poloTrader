from app.strategies.BaseStrategy import BaseStrategy

class MovingAverages(BaseStrategy):

	def __init__(self):
		super().__init__()
		self.registerFunction(self.onEnd)

	"""
	Called once at the start of the algorithm.
	"""
	def initialize(self):
		return

	"""
	Called every configured tick.
	"""
	def onData(self):
		print("MovingAverages.onData() -> ", self.data.historic("BTC_ETH", "open", 1, 300))
		self.order("BTC_ETH", 1, 0.11)
		return

	"""
	Called when the loop ends
	"""
	def onEnd(self):
		return
