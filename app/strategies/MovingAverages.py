from app.strategies.BaseStrategy import BaseStrategy

class MovingAverages(BaseStrategy):

	def __init__(self, dataQueue, orderQueue):
		super().__init__(dataQueue, orderQueue)
		self.registerFunction(self.onEnd)

	"""
	Called once at the start of the algorithm.
	"""
	def initialize(self):
		return

	"""
	Called every time new data is available, what is about once a second.
	"""
	def onData(self):
		print("MovingAverages.onData() -> ", self.data.current(["BTC_ETH"], ['average']))
		self.order("BTC_ETH", 1, 0.11)
		return

	"""
	Called when the loop ends
	"""
	def onEnd(self):
		return
