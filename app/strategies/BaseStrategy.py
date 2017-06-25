from collections import deque
from app.util.DataFrame import Data
from operator import attrgetter
from app.util.Order import Order, OrderMode

class BaseStrategy(object):

	registeredFunctions = list()
	context = "context"
	_data = Data()
	data = property(attrgetter("_data"))
	orderQueue = deque()

	def __init__(self):
		self.registerFunction(self.onData)
		self.registerFunction(self.initialize)
		self.registerFunction(self.getOrderQueue)

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

	def getData(self):
		return self._data

	# TODO: implement order functions
	def getOrderQueue(self):
		return self.orderQueue

	"""
	Places an order for the specified asset and the specified amount of shares

	@param asset: An Equity object or a Future object.
	@param amount: The integer amount of shares or contracts. Positive means buy, negative means sell.
	@param rate: The specified rate to trade at
	@param mode: TODO
	@return: An order id.
	"""
	def order(self, asset, amount, rate, mode = OrderMode.NORMAL):
		order = Order(asset, rate, amount, mode)
		self.orderQueue.append(order)
		return # TODO: get order id

	"""
	Place an order by desired value rather than desired number of shares.
	Placing a negative order value will result in selling the given value.
	Orders are always truncated to whole shares or contracts.

	@param asset: An Equity object or a Future object.
	@param amount: Floating point dollar value of shares or contracts. Positive means buy, negative means sell.
 	@return: An order id.
	"""
	def order_value(self, asset, amount, rate):
		return

	"""
	Places an order in the specified asset corresponding to the given percent of
	the current portfolio value, which is the sum of the positions value and
	ending cash balance. Placing a negative percent order will result in selling
	the given percent of the current portfolio value. Orders are always truncated
	to whole shares or contracts. Percent must be expressed as a decimal
	(0.50 means 50%).

	The value of a position in a futures contract is computed to be the unit
	price times the number of units per contract (otherwise known as the size
	of the contract).

	@param asset: An Equity object or a Future object.
	@param amount: The floating point percentage of portfolio value to order. Positive means buy, negative means sell.
 	@return: An order id.
	"""
	def order_percent(self, asset, amount):
		return

	"""
	Places an order to adjust a position to a target number of shares. If there
	is no existing position in the asset, an order is placed for the full target
	number. If there is a position in the asset, an order is placed for the
	difference between the target number of shares or contracts and the number
	currently held. Placing a negative target order will result in a short
	position equal to the negative number specified.

	@param asset: An Equity object or a Future object.
	@param amount: The integer amount of target shares or contracts. Positive means buy, negative means sell.
 	@return: An order id, or None if there is no difference between the target position and current position.
	"""
	def order_target(self, asset, amount):
		return

	"""
	Places an order to adjust a position to a target value. If there is no
	existing position in the asset, an order is placed for the full target
	value. If there is a position in the asset, an order is placed for the
	difference between the target value and the current position value. Placing
	a negative target order will result in a short position equal to the
	negative target value. Orders are always truncated to whole shares or
	contracts.

	The value of a position in a futures contract is computed to be the unit
	price times the number of units per contract (otherwise known as the size
	of the contract).

	@param asset: An Equity object or a Future object.
	@param amount: Floating point dollar value of shares or contracts. Positive means buy, negative means sell.
 	@return: An order id, or None if there is no difference between the target position and current position.
	"""
	def order_target_value(self, asset, amount):
		return

	"""
	Place an order to adjust a position to a target percent of the current
	portfolio value. If there is no existing position in the asset, an order is
	placed for the full target percentage. If there is a position in the asset,
	an order is placed for the difference between the target percent and the
	current percent. Placing a negative target percent order will result in a
	short position equal to the negative target percent. Portfolio value is
	calculated as the sum of the positions value and ending cash balance.
	Orders are always truncated to whole shares, and percentage must be
	expressed as a decimal (0.50 means 50%).

	The value of a position in a futures contract is computed to be the unit
	price times the number of units per contract (otherwise known as the size
	of the contract).

	@param asset: An Equity object or a Future object.
	@param percent: The portfolio percentage allocated to the asset. Positive
		means buy, negative means sell.
 	@return: An order id, or None if there is no difference between the target
		position and current position.
	"""
	def order_target_percent(self, asset, percent):
		return

	"""
	Attempts to cancel the specified order. Cancel is attempted asynchronously.

	@param order: Can be the order_id as a string or the order object.
	@return: None
	"""
	def cancel_order(self, order):
		return

	"""
	If asset is None or not specified, returns all open orders. If asset is
	specified, returns open orders for that asset

	@param sid: (optional) An Equity object or a Future object. Can be also be None.
	@return: If asset is unspecified or None, returns a dictionary keyed by
		asset ID. The dictionary contains a list of orders for each ID, oldest
		first. If an asset is specified, returns a list of open orders for that
		asset, oldest first.
	"""
	def get_open_orders(self, sid):
		return

	"""
	Returns the specified order. The order object is discarded at the end of
	handle_data.

	@param order: Can be the order_id as a string or the order object.
	@return: returns an order object that is read/writeable but is discarded at
		the end of handle_data.
	"""
	def get_order(self, order):
		return
