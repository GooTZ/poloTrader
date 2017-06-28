import time
import datetime
import os
import csv
import poloniex
from app.util.DataProviders.DataProvider import DataProvider
from app.util.Timing import TimePeriod

class HistoryDataProvider(DataProvider):

	# TODO: read from config
	DATA_DIR = "./data"

	datafilePath = ""
	timefilePath = ""
	newfile = None

	start_time = 0
	end_time = 0

	candle = {}

	timeOfLastFileWrite = time.monotonic()
	timeOfLastSpin = time.monotonic()

	header = ['date', 'low', 'open', 'average', 'close', 'high', 'volume', 'isFrozen']
	data = {}

	pair = ""

	def __init__(self, APIKey, Secret, dataQueue, orderQueue, instructionQueue):
		super().__init__(APIKey, Secret, dataQueue, orderQueue, instructionQueue)
		self.init()

	def init(self):
		# TODO: read config, needs pairs to be fetched
		self.pair = "BTC_LTC"

		self.datafilePath = os.path.join(self.DATA_DIR, self.pair + ".csv")
		self.timefilePath = os.path.join(self.DATA_DIR, "." + self.pair)

		if not os.path.exists(self.DATA_DIR):
			os.mkdir(self.DATA_DIR)

		if os.path.exists(self.datafilePath):
			self.newfile = False
			start_time = int(open(self.timefilePath).readline()) + 1
		else:
			self.newfile = True
			start_time = 1388534400     # 2014.01.01
		end_time = 9999999999 # start_time + 86400*30

	def doTheLoop(self):
		# Once a second print the wip string
		timeofThisLoop = time.monotonic()
		deltaSecond = self.timeOfLastSpin - timeofThisLoop
		if deltaSecond > -(1):
			return # next iteration if not enough time passed
		self.timeOfLastSpin = timeofThisLoop
		print("Fetching data " + self.getSpinner(), end = "\r")

		tickerData = self.getTickerData(self.pair)
		t = int(time.time())
		self.appendToCandle(t, tickerData)

		deltaMinute = self.timeOfLastTickFetch - timeofThisLoop
		if deltaMinute > -60:
			return # next iteration if not enough time passed
		self.timeOfLastTickFetch = timeofThisLoop

		self.appendCandleToData(self.candle)
		self.candle.clear()

		# execute this part of the loop only once every 30 minutes
		delta60Min = self.timeOfLastFileWrite - timeofThisLoop
		if delta60Min > -(60 * 30):
			return # next iteration if not enough time passed
		self.timeOfLastFileWrite = timeofThisLoop

		self.writeDataToFile()

		"""
		# execute this part of the loop only once every 5 minutes
		delta5Min = self.timeOfLastCandlestickFetch - timeofThisLoop
		if delta5Min > -(TimePeriod.T300.value):
			return # next iteration if not enough time passed
		self.timeOfLastCandlestickFetch = timeofThisLoop

		chartData = self.getChartData(self.pair)
		for dataset in chartData:
			time_index = int(dataset['date'])
			self.appendToData(time_index, dataset)
		"""

	def getChartData(self, pair, start_time = None, end_time = None):
		if start_time == None and end_time == None:
			start_time = self.start_time
			end_time = self.end_time

		chartData = self.polo.returnChartData(pair, period = 300, start = start_time, end = end_time)
		return chartData

	def getTickerData(self, pair):
		tickerData = self.polo.returnTicker()
		return tickerData[pair]

	def appendToData(self, date, data):
		dataDict = {}
		for item in self.header:
			if item in data:
				dataDict[item] = data[item]
			else:
				dataDict[item] = 0
		dataDict['date'] = date
		self.data[date] = dataDict

	def writeDataToFile(self):
		end_time = 0
		with open(self.datafilePath, 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

			if self.newfile:
				spamwriter.writerow(self.header)

			for dr in self.data:
				row = []
				end_time = dr
				for v in self.data[dr]:
					row.append(self.data[dr][v])
				spamwriter.writerow(row)

		with open(self.timefilePath, "w") as ft:
			ft.write("%d\n" % end_time)
			ft.close()

		self.data.clear()

		print(datetime.datetime.utcnow())
		print("data written")

	def appendCandleToData(self, candle):
		dataDict = {'date': candle['date'], 'low': candle['low'], 'open': candle['open'], 'average': candle['average'] / self.c,
		'close': candle['close'], 'high': candle['high'], 'volume': candle['volume'] / self.c, 'isFrozen': candle['isFrozen']}
		print(dataDict)
		self.data[candle['date']] = dataDict
		self.secondsPassed = 0
