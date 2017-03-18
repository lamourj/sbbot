import connexion ## TODO: fix import

class DayTable:
    """
    Handles set of user to care about for a specific day and which trains
    users are interested in.
    """


    def __init__(self, isRegular):
        """
        isRegular == True if this table stores regular connexions.
        """
        self.table = dict()
        self.isRegular = isRegular


    def addConnexionForDay(self, uid, tid, connexion):
        """
        Add a connexion for this day for specific user.
        """
        if tid not in self.table:
            self.table[tid] = []
        if uid not in self.table[tid]:
            self.table[tid].append((uid, connexion))