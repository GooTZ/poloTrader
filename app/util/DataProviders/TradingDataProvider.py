import time
import poloniex
from app.util.DataProviders.DataProvider import DataProvider

class TradingDataProvider(DataProvider):

    def __init__(self, APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue):
        super().__init__(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)

    def doTheLoop(self):
        # Once a second print the fetching-data string
        timeofThisLoop = time.monotonic()
        delta = self.timeOfLastOrder - timeofThisLoop
        if delta > -1:
            return # next iteration if not enough time passed
        self.timOfLastOrder = timeofThisLoop
        print("Fetching data " + self.getSpinner(), end = "\r")

        tickerData = self.getTickerData()
        t = int(time.time())
        for pair in tickerData:
            self.appendToCandle(t, pair, tickerData[pair])
        self.secondsPassed += 1

        balances = self.polo.returnBalances()
        self.dataQueue.put(("Balances", balances))

        if not (self.orderQueue.empty()):
            order = self.orderQueue.get()
            self.placeOrder(order)

        deltaMinute = self.timeOfLastTickFetch - timeofThisLoop
        if deltaMinute > -60:
            return # next iteration if not enough time passed
        self.timeOfLastTickFetch = timeofThisLoop

        self.appendCandlesToData()
        self.currentCandles = {}

    def appendCandlesToData(self):
        outrDict = {}
        for pair in self.currentCandles:
            candle = self.currentCandles[pair]
            print(candle['average'])
            dataDict = {'date': candle['date'], 'low': candle['low'], 'open': candle['open'], 'average': candle['average'] / self.secondsPassed,
            'close': candle['close'], 'high': candle['high'], 'volume': candle['volume'] / self.secondsPassed, 'isFrozen': candle['isFrozen']}
            outrDict[pair] = dataDict
        self.dataQueue.put(("Current", outrDict))
        self.secondsPassed = 0

    def placeOrder(self, order):
        amount = abs(order.amount)
        rate = abs(order.rate)
        orderNmbr = 0
        if order.amount < 0:
            if order.mode == OrderMode.NORMAL:
                orderNmbr = self.polo.sell(order.pair, rate, amount)
            else:
                orderNmbr = self.polo.sell(order.pair, rate, amount, order.mode.value)
        elif order.amount > 0:
            if order.mode == OrderMode.NORMAL:
                orderNmbr = self.polo.buy(order.pair, rate, amount)
            else:
                orderNmbr = self.polo.buy(order.pair, rate, amount, order.mode.value)
