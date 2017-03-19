class TrainTable:
	"""
	Class to store trains and their departure and arrival times
	"""

	def __init__(self):
		self.table = dict()

	def addConnexion(self, connexion):
		if connexion.tid not in self.table:
			print('not in table yet')
			self.table[connexion.tid] = (connexion.departureTime, connexion.arrivalTime)
		else:
			currentTimes = self.table[tid]
			newTimes = (min(currentTimes[0], connexion.departureTime), min(currentTimes[1], connexion.arrivalTime))
			if not newTime == currentTimes:
				self.table[connexion.tid] = newTimes

		print('now added in table: ' + str(self.table[connexion.tid]))
		print('inside train_table: ' + str(self.table))

	def getTimesForTid(self, tid):
		"""
		Returns a pair containing departureTime and arrivalTime for given tid.
		"""
		if tid in self.table:
			return self.table[tid]
		else:
			return None