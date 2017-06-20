# SimpleEmaStrategy.py created on 16/6/2017 by Domenik Weber

from enum import Enum

class Action(Enum):
	SELL = -1
	HOLD = 0
	BUY = 1

class Names(Enum):
	EMA5 = int(5)
	EMA35 = int(35)

class TradingStrategy(object):

	btc = float(0.00118118)
	eth = float(0)

	payoffPercentage = 0.0005
	currentPrice = None
	buyPrice = -1

	movingAveragesMaxSize = 10
	movingAverages = list()

	candlesticksMaxSize = 36
	candlesticks = list()

	priceTicksMaxSize = 10
	priceTicks = list()

	def __init__(self):
		print("instantiated TradingStrategy!")

	def buyingCriteria(self):
		return list([
		(self.movingAverages[0][Names.EMA5] < self.movingAverages[0][Names.EMA35]),
		(self.movingAverages[1][Names.EMA5] < self.movingAverages[0][Names.EMA5]),
		(self.btc > float(0))
		])

	def sellingCriteria(self):
		return list([
		(self.movingAverages[0][Names.EMA5] > self.movingAverages[0][Names.EMA35]),
		(self.movingAverages[0][Names.EMA5] - self.movingAverages[0][Names.EMA35] >= self.buyPrice * self.payoffPercentage),
		(self.movingAverages[1][Names.EMA5] > self.movingAverages[0][Names.EMA5]),
		(self.buyPrice < self.currentPrice),
		(self.eth > float(0))
		])

	def addNewCandlestick(self, candlestick):
		for c in candlestick:
			self.candlesticks.insert(0, float(c))
		if (len(self.candlesticks) > self.candlesticksMaxSize):
			self.candlesticks.pop()
		self.onNewCandlestick()

	def onNewCandlestick(self):
		self.updateEmas()
		# Only trade when all data is set up
		if (len(self.candlesticks) == self.candlesticksMaxSize and not self.currentPrice == None):
			self.makeTradingDecision()

	def addNewTick(self, tick):
		for t in tick:
			self.priceTicks.append(t)
		if (len(self.priceTicks) > self.priceTicksMaxSize):
			self.priceTicks[self.priceTicksMaxSize:len(self.priceTicks) - 1] = []
		self.onNewTick()

	def onNewTick(self):
		self.updatePrice()

	def sma(self, timeSteps):
		summe = 0
		index = 0
		while index <= len(self.candlesticks) - 1:
			summe += self.candlesticks[index]
			index += 1
		return summe / timeSteps

	def ema(self, timeSteps):
		# If there is no ema for yesterday, take todays sma as yesterday
		# TODO: kinda hacky, rework the way movingAverages are set up in the first place
		if (len(self.movingAverages) <= 1):
			self.movingAverages.insert(0, {Names.EMA5: self.sma(5), Names.EMA35: self.sma(35)})
			self.movingAverages.insert(1, {Names.EMA5: self.sma(5), Names.EMA35: self.sma(35)})

		multiplier = (2 / (timeSteps + 1) )
		close = self.candlesticks[0]
		ema = (close - self.movingAverages[1][Names(timeSteps)]) * multiplier + self.movingAverages[1][Names(timeSteps)]

		return ema

	def updateEmas(self):
		self.movingAverages.insert(0, {Names.EMA5: self.ema(5), Names.EMA35: self.sma(35)})
		if (len(self.movingAverages) > self.movingAveragesMaxSize):
			self.movingAverages.pop()

	def updatePrice(self):
		summe = 0
		for price in self.priceTicks:
			summe += price
		self.currentPrice = summe / len(self.priceTicks)

	def decideBuy(self):
		# TODO: implement me
		self.buyPrice = self.currentPrice
		self.eth = self.btc / self.buyPrice
		self.btc = 0.0
		print("buying eth at ", self.currentPrice, "ETH: ", self.eth)
		return (Action.BUY, self.currentPrice, 0)

	def decideSell(self):
		# TODO: implement me
		self.btc = self.eth * self.currentPrice
		self.eth = 0.0
		print("selling eth at ", self.currentPrice, "BTC: ", self.btc)
		return (Action.SELL, self.currentPrice, 0)

	def decideHold(self):
		# TODO: implement me
		#print("decideHold")
		return (Action.HOLD)

	def makeTradingDecision(self):
		buy = True
		for c in self.buyingCriteria():
			if not c:
				buy = False
				break

		if buy:
			return self.decideBuy()

		sell = True
		for c in self.sellingCriteria():
			if not c:
				sell = False
				break

		if sell:
			return self.decideSell()

		return self.decideHold()

if __name__ == "__main__":
	print("This file should not be executed on its own!")
	exit()
