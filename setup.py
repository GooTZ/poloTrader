from setuptools import setup

setup(
	# Application name:
	name = "poloTrader",

	# Version number (initial):
	version = "0.1.0",

	# Application author details:
	author = "Domenik Weber",
	author_email = "domenik.weber@stud.uni-hannover.de",

	# Packages
	packages = ["app"],

	# Details
	url = "https://github.com/GooTZ/poloTrader",

	#
	# license="LICENSE.txt",
	description = "A Poloniex altcoin trading software",

	dependency_links = [
		"https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.5.tar.gz#egg=poloniex-0.4.5"
		],

	install_requires = [
		'toml',
		'poloniex>=0.4.5'
	]
)
