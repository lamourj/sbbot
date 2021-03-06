class TrainTable:
    """
    Class to store trains and their departure and arrival times
    """

    def __init__(self):
        self.table = dict()

    def addConnexion(self, connexion):
        if connexion.tid not in self.table:
            self.table[connexion.tid] = (connexion.departureTime, connexion.arrivalTime)
        else:
            currentTimes = self.table[connexion.tid]
            newTimes = (min(currentTimes[0], connexion.departureTime), min(currentTimes[1], connexion.arrivalTime))
            if (True):
                self.table[connexion.tid] = newTimes


    def getTimesForTid(self, tid):
        """
        Returns a pair containing departureTime and arrivalTime for given tid.
        """
        if tid in self.table:
            return self.table[tid]
        else:
            return None