import logging

class Context(object):
	portfolio = {}

class Data(object):
	_current = dict()

	_historic = dict()

	_portfolio = dict()

	def __init__(self):
		self._price = 100

	def current(self, assets, fields):
		if (assets in self._current) and (fields in self._current[assets]):
			return self._current[assets][fields]
		else:
			warning = "Data " + str(assets) + " " + str(fields) + " could not be found!"
			logging.warning(warning)
			return None

	def historic(self, assets, fields, bar_count, frequency):
		# TODO: support the frequency properly
		if (assets in self._historic) and (fields in self._historic[assets]) and (bar_count <= len(_historic)):
			# TODO: Return in format of: dict[asset][bar_count][fields]
			return _historic["""bar_count"""][assets]
		else:
			warning = "Data " + str(assets) + " " + str(fields) + " could not be found!"
			logging.warning(warning)
			return None

	def portfolio(self, assets = None):
		if assets == None:
			return self._portfolio

		p = dict()
		for asset in assets:
			if asset in self._portfolio:
				p[asset] = self._portfolio[asset]

		return p

	def can_trade(self, assets):
		can_trade = True
		for asset in assets:
			if not self._current[assets]['isFrozen']:
				can_trade = False
		return can_trade

	def updateCurrent(self, pair, newCurrent):
		self._current[pair] = newCurrent

	def updatePortfolio(self, portfolio):
		self._portfolio = portfolio
