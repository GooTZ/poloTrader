import app
import sys, getopt
from app.util.TradingMode import TradingMode

def main(argv):
	mode = ''
	try:
		opts, args = getopt.getopt(argv,"m:h",["mode="])
	except getopt.GetoptError:
		print('run.py -m <testing/livetesting>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('run.py -m <testing/livetesting>')
			sys.exit()
		elif opt in ("-m", "--mode"):
			if arg in TradingMode.__members__:
				mode = TradingMode[arg]
			else:
				print(arg, " is not an supported mode!")
				exit(2)

	app.run(mode)


if __name__ == "__main__":
	main(sys.argv[1:])
