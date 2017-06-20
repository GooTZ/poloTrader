import app
import sys, getopt

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
			# TODO: check if mode is supported
			mode = arg

	app.run(mode)


if __name__ == "__main__":
	main(sys.argv[1:])
