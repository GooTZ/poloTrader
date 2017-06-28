from app.util.DataProviders.DataProvider import DataProvider

class TestingDataProvider(DataProvider):

	def __init__(self, APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue):
		super().__init__(APIKey, Secret, dataDir, dataQueue, orderQueue, instructionQueue)

	# TODO: implement base functions and get data from csv tables
