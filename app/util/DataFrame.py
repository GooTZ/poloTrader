from operator import attrgetter

class Context(object):
	portfolio = {}

class Data(object):
	_current = dict()

	_historic = dict()

	def __init__(self):
		self._price = 100

	def current(self, assets, fields):
		if (assets in self._current) and (fields in self._current[assets]):
			return _current[assets][fields]
		else:
			# TODO: log 'data can not be found' on WARNING
			return None

	def historic(self, assets, fields, bar_count, frequency):
		# TODO: support the frequency properly
		if (assets in self._historic) and (fields in self._historic[assets]) and (bar_count <= len(_historic)):
			# TODO: Return in format of: dict[asset][bar_count][fields]
			return _historic["""bar_count"""][assets]
		else:
			# TODO: log 'data can not be found' on WARNING
			return None

	# TODO: implement this properly
	def can_trade(self, assets):
		can_trade = True
		for asset in assets:
			can_trade = True
		return can_trade

"""
class Current(object):
	_last = None
	last = property(attrgetter("_last"))

	_lowestAsk = None
	lowestAsk = property(attrgetter("_lowestAsk"))

	_highestBid = None
	highestBid = property(attrgetter("_highestBid"))

	_percentChange = None
	percentChange = property(attrgetter("_percentChange"))

	_baseVolume = None
	baseVolume = property(attrgetter("_baseVolume"))

	_quoteVolume = None
	quoteVolume = property(attrgetter("_quoteVolume"))

	def __init__(self):
		return
"""
