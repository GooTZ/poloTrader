import sys, getopt

import app
from app.util.TradingMode import TradingMode
from app.util.Error import *

def main(argv):
    mode = ''
    try:
        opts, args = getopt.getopt(argv,"m:h",["mode="])
    except getopt.GetoptError:
        print('run.py -m <TESTING/LIVE_TESTING/TRADING/FETCH_DATA>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('run.py -m <TESTING/LIVE_TESTING/TRADING/FETCH_DATA>')
            sys.exit()
        elif opt in ("-m", "--mode"):
            if arg in TradingMode.__members__:
                mode = TradingMode[arg]
            else:
                raise UnsupportedModeError(arg, "The given mode is not supported!")

    app.run(mode)


if __name__ == "__main__":
    main(sys.argv[1:])
