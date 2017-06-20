from distutils.core import setup

setup(
	# Application name:
	name="poloTrader",

	# Version number (initial):
	version="0.1.0",

	# Application author details:
	author="Domenik Weber",
	author_email="domenik.weber@stud.uni-hannover.de",

	# Packages
	packages=["app"],

	# Include additional files into the package
	include_package_data=True,

	# Details
	url="https://github.com/GooTZ/poloTrader",

	#
	# license="LICENSE.txt",
	description="A Poloniex altcoin trading software",

	# long_description=open("README.txt").read(),

	# Dependent packages (distributions)
	install_requires=[
		'poloniex'
	],

	dependency_links=[
		'https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.4.zip'
	]
)
