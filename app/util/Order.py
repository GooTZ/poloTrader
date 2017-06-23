from enum import Enum

		
class OrderMode(Enum):
	NORMAL = 0
	FILL_OR_KILL = 1
	IMMEDIATE_OR_CACNEL = 2
	POST_ONLY = 3

class Order(object):
	
	def __init__(self, pair, rate, amount, mode = OrderMode.NORMAL):
		self.pair = pair
		self.rate = rate
		self.amount = amount
		self.mode = mode
		
	def __str__(self):
		s = "(Order: " + str(self.pair) + ", " + str(self.rate) + ", " + str(self.amount) + ", " + str(self.mode) + ")"
		return s
		
	def setOrderNumber(self, number):
		self.orderNumber = number
		
	def getOrderNumber(self):
		return self.orderNumber
