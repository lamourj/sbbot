from day_table import DayTable
from connexion import Connexion

class TablesManager:
    """Manages tables for days of week"""
    validDaysOfWeek = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    def __init__(self):
        """
        Initializes one table for each day of the week for
        regular journeys.
        Initializes a dict of tables for singular entries.
        """

        self.regularTables = dict()
        for dayOfWeek in validDaysOfWeek:
            self.regularTables[dayOfWeek] = DayTable(isRegular=True)
        
        self.singularTables = dict()

    def addRegularEntry(self, dayOfWeek, tid, uid, connexion):
        """
        Adds the specified regular connexion for specified train ID (tid) 
        and user ID (uid) at the singular day of week (mon, tue, wed, thu,
        fri, sat, sun).
        """
        self.regularTables[dayOfWeek].addConnexionForDay(uid, tid, connexion)

    def addSingularEntry(self, dayOfYear, tid, uid, connexion):
        """
        Adds the specified singular connexion for specified train ID (tid)
        and user ID (uid) at the singular day of year (1,...,365)
        """
        if dayOfYear not in self.singularTables:
            self.singularTables[dayOfYear] = DayTable(isRegular=False)
        self.singularTables[dayOfYear].addConnexionForDay(uid, tid, connexion)


    def getRegularTableForDayOfWeek(self, dayOfWeek):
        """
        Returns the regular table for the specified day of the week.
        """
        assert dayOfWeek in validDaysOfWeek, dayOfWeek + " is not a valid day of week."
        return self.regularTables[dayOfWeek]

    def getSingularTableForDayOfYear(self, dayOfYear):
        """
        Returns the singular table for the specified day of year or None
        if there is none specified.
        """
        assert dayOfYear >= 0 and dayOfYear < 366, str(dayOfYear) + " is not a valid day expected: 0 <= dayOfYear < 366."
        if dayOfYear in self.singularTables:
            return self.singularTables[dayOfYear]
        else:
            return None