from .connexion import Connexion 

class DayTable:
    """
        Handles set of user to care about for a singular day and which trains
        users are interested in.
    """

    def __init__(self, table=None):
        if(table==None):
            self.table = dict()
        else:
            self.table = table.copy()

    def addConnexionForDay(self, tid, uid, connexion):
        """
        Adds a connexion for this day for singular user.
        """
        if tid not in self.table:
            self.table[tid] = []
        if uid not in self.table[tid]:
            self.table[tid].append((uid, connexion))

    def getUsersAndConnexionsForTid(self, tid):
        """
        Returns the pairs of (uid, connexion) that are
        using the train having the specified tid or []
        if there is no users for this train.
        """

        if tid in self.table:
            return self.table[tid]
        else:
            return []

    def getTable(self):
        return self.table.copy()