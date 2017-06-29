import logging

class Context(object):
	portfolio = {}

class Data(object):
	_current = dict()

	_historic = []

	_portfolio = dict()

	def __init__(self):
		self._price = 100

	"""
	Returns the current value of the given assets for the given fields at the current algorithm time. Current values are the as-traded price.

	@param assets: An array of traded currency pairs.
	@param fields: An array of Strings. Valid fields are 'date', 'low', 'open', 'average', 'close', 'high', 'volume' and 'isFrozen'.
	@returns: An dictionary of the given assets containing dictionaries of the given fields.
	"""
	def current(self, assets, fields):
		p = dict()
		for asset in assets:
			for field in fields:
				if (asset in self._current) and (field in self._current[asset]):
					if not asset in p:
						p[asset] = {}
					p[asset][field] = self._current[asset][field]
				else:
					warning = "Data " + str(assets) + " " + str(fields) + " could not be found!"
					logging.warning(warning)
					return None
		return p

	"""
	Returns the last n bars of the given assets and fields with 'bar_count' as n.

	@param assets: An array of traded currency pairs.
	@param fields: An array of Strings. Valid fields are 'date', 'low', 'open', 'average', 'close', 'high', 'volume' and 'isFrozen'.
	@param bar_count: Integer number of bars to return.
	@param frequency: A field of the FREQUENCY enum.
	"""
	def historic(self, assets, fields, bar_count, frequency):
		# TODO: support frequency properly
		p = dict()
		hist_len = len(self._historic)
		for i in reversed(range(0, hist_len)):
			for asset in assets:
				#p[asset] = dict()
				fields_dict = dict()
				for field in fields:
					if (bar_count > hist_len):
						warning = str(bar_count) + " is out of range of the history!"
						logging.warning(warning)
						return None

					if not ((asset in self._historic[i]) and (field in self._historic[i][asset])):
						warning = "Data " + str(asset) + "." + str(field) + " could not be found!"
						logging.warning(warning)
						return None

					fields_dict[field] = self._historic[i][asset][field]

				t = self._historic[i][asset]['date']
				if (t not in p):
					p[t] = dict()
				p[t][asset] = fields_dict
		return p

	"""
	Returns a dictionary with the amount of coins given by the argument.

	@param assets: An Array of traded coins.
	@returns: Dictionary with the amount of coins indexed by the coin name.
	"""
	def portfolio(self, assets = None):
		if assets == None:
			return self._portfolio

		p = dict()
		for asset in assets:
			if asset in self._portfolio:
				p[asset] = self._portfolio[asset]

		return p

	"""
	For the given array of coinpairs, return a corresponding dictionary of booleans. Boolean is true if the coinpair can be traded, false if not.

	@param assets: Array of coinpairs.
	@returns: Dictionary of booleans, corresponding to the tradability.
	"""
	def can_trade(self, assets):
		can_trade = dict()
		for asset in assets:
			if not self._current[assets]['isFrozen']:
				can_trade[asset] = False
			else:
				can_trade[asset] = True
		return can_trade

	def updateCurrent(self, newCurrent):
		self._historic.append(self._current)
		for pair in newCurrent:
			self._current[pair] = newCurrent[pair]

	def updatePortfolio(self, portfolio):
		self._portfolio = portfolio
