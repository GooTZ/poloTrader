from app.util.DataProviders.DataProvider import DataProvider

class TestingDataProvider(DataProvider):

	def __init__(self, APIKey, Secret):
		super().__init__(APIKey, Secret)

	# TODO: implement base functions and get data from csv tables
