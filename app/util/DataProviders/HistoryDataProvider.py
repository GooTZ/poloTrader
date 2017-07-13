import time
import datetime
import os
import csv
import poloniex
from app.util.DataProviders.DataProvider import DataProvider
from app.util.Timing import TimePeriod

class HistoryDataProvider(DataProvider):

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

    pairs = {}

    def __init__(self, APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue):
        super().__init__(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)
        self.init()

    def init(self):
        if not os.path.exists(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)

        volume = polo.return24hVolume()
        for pair in volume:
            self.pairs[pair] = lookupTimefile(pair)

        # TODO: load missing data from last date to now
        

    def doTheLoop(self):
        # Once a second print the wip string
        timeofThisLoop = time.monotonic()
        deltaSecond = self.timeOfLastSpin - timeofThisLoop
        if deltaSecond > -(1):
            return # next iteration if not enough time passed
        self.timeOfLastSpin = timeofThisLoop
        print("Fetching data " + self.getSpinner(), end = "\r")

        tickerData = self.getTickerData()
        t = int(time.time())
        for pair in tickerData:
            self.appendToCandle(t, pair, tickerData[pair])
        self.secondsPassed += 1

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

    def lookupTimefile(self, pair):
        datafilePath = os.path.join(self.DATA_DIR, self.pair + ".csv")
        timefilePath = os.path.join(self.DATA_DIR, "." + self.pair)

        if os.path.exists(self.datafilePath):
            self.newfile = False
            start_time = int(open(self.timefilePath).readline()) + 1
        else:
            self.newfile = True
            start_time = 1388534400     # 2014.01.01
        end_time = 9999999999 # start_time + 86400*30

        return {"datafilePath": datafilePath, "startTime": start_time, "endTime": end_time}

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
        dataDict = {'date': candle['date'], 'low': candle['low'], 'open': candle['open'], 'average': candle['average'] / self.secondsPassed,
        'close': candle['close'], 'high': candle['high'], 'volume': candle['volume'] / self.secondsPassed, 'isFrozen': candle['isFrozen']}
        print(dataDict)
        self.data[candle['date']] = dataDict
        self.secondsPassed = 0
