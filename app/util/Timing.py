import time
import datetime
from enum import IntEnum

def getHistoricTimestamp(day = 0, hour = 0, minute = 0):
    time = datetime.datetime.utcnow() - datetime.timedelta(days = day, hours = hour, minutes = minute)
    return time.timestamp()

class TimePeriod(IntEnum):
    T300 = int(300)
    T900 = int(900)
    T1800 = int(1800)
    T7200 = int(7200)
    T14400 = int(14400)
    T86400 = int(86400)
