import logging

class Context(object):
	portfolio = {}

class Data(object):
	_current = dict()

	_historic = []

	_portfolio = dict()

	def __init__(self):
		self._price = 100

	def current(self, assets, fields):
		p = dict()
		for asset in assets:
			for field in fields:
				if (asset in self._current) and (field in self._current[asset]):
					p[asset] = self._current[asset]
				else:
					warning = "Data " + str(assets) + " " + str(fields) + " could not be found!"
					logging.warning(warning)
					return None
		return p

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
		self._historic.append(self._current)
		self._current[pair] = newCurrent
		self._current["BTC_LTC"] = newCurrent

	def updatePortfolio(self, portfolio):
		self._portfolio = portfolio
