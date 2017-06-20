# dataProvider.py created on 16/6/2017 by Domenik Weber

import poloniex
import csv
import time
import datetime
import yaml

import SimpleEmaStrategy

class DataProvider(object):
	polo = None
	
	APIKey = ""
	Secret = ""

	pair = None
	chartData = list()
	tickData = list()

	testing = None
	csvData = list()

	doc = None

	strategy = SimpleEmaStrategy.TradingStrategy()

	def __init__(self, pair, testing):
		print("DataProvider instantiated")

		with open('config.yaml', 'r') as f:
			doc = yaml.load(f)

		self.APIKey = doc["api"]["key"]
		self.Secret = doc["api"]["secret"]

		self.polo = poloniex.Poloniex()
		# or
		self.polo.key = self.APIKey
		self.polo.secret = self.Secret

		self.pair = pair
		self.testing = testing

		if (testing):
			with open(self.pair + '.csv', newline='') as f:
				reader = csv.reader(f)
				next(reader)
				for row in reader:
					self.csvData.append(row)
				#self.csvData = self.csvData[len(self.csvData) - (3 * 30 * 24 * 12):]

	def unixBackInTime(self, minutesToGoBack):
		current_time = datetime.datetime.now()
		backInTime = self.getUnixTimestamp(current_time) - (minutesToGoBack * 60)  # 5 min * 60 seconds
		return backInTime

	def getUnixTimestamp(self, time):
		return time.timestamp() # works if Python >= 3.3

	def fetchNewChartData(self, period, start):
		data = self.polo.returnChartData(self.pair, period = period, start = start, end = 9999999999)

		for d in data:
			# no need to add data if there is no data
			if(d['close'] == 0):
				return

			# don't add data if there is no new data
			# TODO: try weightedAverage instead of close
			if(len(self.chartData) - 1 > 0 and self.chartData[len(self.chartData) - 1] == d['close']):
				return

			# add new data to the stack
			self.chartData.insert(0, float(d['close']))

			# resize the stack back to it's max size
			if(35 < len(self.chartData)):
				self.chartData.pop()

		self.onFetchedChartData()

	def onFetchedChartData(self):
		self.strategy.addNewCandlestick(self.chartData)
		self.chartData.clear()

	def fetchNewTickData(self):
		data = self.polo.marketTradeHist(currencyPair = self.pair)
		data = data[:10]

		for d in data:
			# no need to add data if there is no data
			if(d['rate'] == 0):
				return

			# don't add data if there is no new data
			if(len(self.tickData) - 1 > 0 and self.tickData[len(self.tickData) - 1] == d['rate']):
				return

			# add new data to the stack
			self.tickData.insert(0, float(d['rate']))

			# resize the stack back to it's max size
			if(10 < len(self.tickData)):
				self.tickData.pop()

		self.onFetchedTickData()

	def onFetchedTickData(self):
		self.strategy.addNewTick(self.tickData)
		self.tickData.clear()

	def getNewDataFromCsv(self):
		if (len(self.csvData) <= 2):
			print("End of Dataset!")
			exit()

		row1 = self.csvData[1]
		row2 = self.csvData[2]

		# add new data to the stack
		self.tickData.insert(0, float(row1[7]))
		# resize the stack back to it's max size
		if(10 < len(self.tickData)):
			self.tickData.pop()

		# add new data to the stack
		self.chartData.insert(0, float(row2[4]))
		# resize the stack back to it's max size
		if(35 < len(self.chartData)):
			self.chartData.pop()

		self.csvData.pop(0)
		self.onFetchedTickData()
		self.onFetchedChartData()

	def dataLoop(self):
		timeOfLastTickFetch = time.monotonic()
		timeOfLastCandlestickFetch = time.monotonic()

		#int2 = int(self.csvData[len(self.csvData) - 1][0])
		#print(datetime.datetime.fromtimestamp(int2).strftime('%Y-%m-%d %H:%M:%S'))

		while True:
			if self.testing:
				self.getNewDataFromCsv()
				continue

			# execute the rest of the loop only 5 times a second
			# (api is restricted to 6 calls a second, so 5 times to be sure)
			timeofThisLoop = time.monotonic()
			delta1 = timeOfLastTickFetch - timeofThisLoop
			if delta1 > -(1/4):
				continue # next iteration if not enough time passed
			timeOfLastTickFetch = timeofThisLoop

			self.fetchNewTickData()

			# execute the rest of the loop only 1 time a second
			delta2 = timeOfLastCandlestickFetch - timeofThisLoop
			if delta2 > -(1):
				continue # next iteration if not enough time passed
			timeOfLastCandlestickFetch = timeofThisLoop

			self.fetchNewChartData(period = 300, start = self.unixBackInTime(5))

if __name__ == "__main__":
	dataProvider = DataProvider(pair = "BTC_ETH", testing = True)
	dataProvider.dataLoop()
