from day_table import DayTable
from connexion import Connexion
from 

class TablesManager:
    """
    Manages tables for days of week

    All times are in minutes from midnight.
    """
    validDaysOfWeek = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    def __init__(self, currentDayOfWeek, currentDayOfYear):
        """
        Initializes one table for each day of the week for
        regular journeys.
        Initializes a dict of tables for singular entries.
        """

        assert dayOfWeek in validDaysOfWeek, dayOfWeek + " is not a valid day of week."
        assert dayOfYear >= 0 and dayOfYear < 366, str(dayOfYear) + " is not a valid day expected: 0 <= dayOfYear < 366."

        self.regularTables = dict()
        for dayOfWeek in validDaysOfWeek:
            self.regularTables[dayOfWeek] = DayTable()
      
        self.currentDayOfWeek = currentDayOfWeek
        self.currentDayOfYear = currentDayOfYear
        
        self.todaysTrainTable = trainTable()
        self.todaysTable = DayTable()
        self.setTodaysDate(currentDayOfWeek, currentDayOfYear)

    def addRegularEntry(self, dayOfWeek, tid, uid, connexion):
        """
        Adds the specified regular connexion for specified train ID (tid) 
        and user ID (uid) at the singular day of week (mon, tue, wed, thu,
        fri, sat, sun).
        """
        assert dayOfWeek in validDaysOfWeek, dayOfWeek + " is not a valid day of week."

        if dayOfWeek == self.currentDayOfWeek: 
            # If dayOfWeek is today, have to add current travel to today's table
            self.todaysTable.addConnexionForDay(uid, tid, connexion)

        self.todaysTrainTable.addConnexion(connexion)
        self.regularTables[dayOfWeek].addConnexionForDay(uid, tid, connexion)

    def addSingularEntry(self, dayOfYear, tid, uid, connexion):
        """
        Adds the specified singular connexion for specified train ID (tid)
        and user ID (uid) at the singular day of year (1,...,365)
        """
        assert dayOfYear >= 0 and dayOfYear < 366, str(dayOfYear) + " is not a valid day expected: 0 <= dayOfYear < 366."

        if dayOfYear == self.currentDayOfYear: 
            # If dayOfYear is today, have to add current travel to today's table
            self.todaysTable.addConnexionForDay(uid, tid, connexion)


        if dayOfYear not in self.singularTables:
            self.singularTables[dayOfYear] = DayTable()

        self.todaysTrainTable.addConnexion(connexion)

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

    def setTodaysDate(self, currentDayOfWeek, currentDayOfYear):
        """
        Update today's date and update today's table.
        Expensive but should be done only once a day.
        """
        assert currentDayOfWeek in validDaysOfWeek, currentDayOfWeek + " is not a valid day of week."
        assert currentDayOfYear >= 0 and dayOfYear < 366, str(currentDayOfYear) + " is not a valid day expected: 0 <= dayOfYear < 366."

        self.currentDayOfWeek = currentDayOfWeek
        self.currentDayOfYear = currentDayOfYear

        # Build today's tables:
        regularTable = self.regularTables[self.currentDayOfWeek]
        singularTable = self.singularTables[self.currentDayOfYear]
        
        union = {**regularTable.getTable(), **singularTable.getTable()}
        self.todaysTable = DayTable(table=union)

        self.todaysTrainTable = dict()
        for tid in self.todaysTable:
            entries = self.todaysTable[tid]
            for uid, connexion in entries:
                self.todaysTrainTable.addConnexion(tid, connexion)


    def removePastTrains(self, currentTime, delay):
        """
        Removes trains for which train.arrivalTime > currentTime + delay
        from today's trainstable.
        """
        for tid in self.todaysTable:
            if(self.todaysTrainTable.getTimesForTid[1] > currentTime + delay):
                # if train.arrivalTime > currentTime + delay (which delay??), can unlook train TODO delay
                del self.todaysTrainTable[tid]
                del self.todaysTable[tid]


    def getTidsToCheck(self, currentTime, delay):
        """
        Returns all the tid of the trains that are more than +/- delay 
        from now.
        """
        tids = []
        for tid in self.todaysTrainTable:
            departureTime, arrivalTime = self.todaysTrainTable[tid]
            delayToNow = min(abs(departureTime-delay), abs(arrivalTime-delay))
            if(delayToNow > delay):
                tids.append(tid)