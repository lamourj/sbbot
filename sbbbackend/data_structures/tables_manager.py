from .day_table import DayTable
from .train_table import TrainTable
from .connexion import Connexion
from .interfaces import Parser

class TablesManager:
    """
    Manages tables for days of week

    All times are in minutes from midnight.
    """
    def __init__(self, currentDayOfWeek, currentDayOfYear):
        """
        Initializes one table for each day of the week for
        regular journeys.
        Initializes a dict of tables for singular entries.
        """
        self.validDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        assert currentDayOfWeek in self.validDays, currentDayOfWeek + " is not a valid day of week."
        assert currentDayOfYear >= 0 and currentDayOfYear < 366, str(currentDayOfYear) + " is not a valid day expected: 0 <= currentDayOfYear < 366."

        self.regularTables = dict()
        for currentDayOfWeek in self.validDays:
            self.regularTables[currentDayOfWeek] = DayTable()

        self.singularTables = dict()
      
        self.currentDayOfWeek = currentDayOfWeek
        self.currentDayOfYear = currentDayOfYear
        
        self.todaysTrainTable = TrainTable()
        self.todaysTable = DayTable()
        self.setTodaysDate(currentDayOfWeek, currentDayOfYear)

    def addRegularEntry(self, dayOfWeek, uid, json):
        # def __init__(self, tid, departure, arrival, departureTime, arrivalTime):
        sections = Parser.parseConnexion(json)['sections']
        connexions = []
        for section in sections:
            tid = section['tid']
            departure = section['from']
            arrival = section['to']
            departureTime = section['departureTime']
            arrivalTime = section['arrivalTime']
            departurePlatform = section['departurePlatform']
            arrivalPlatform = section['arrivalPlatform']
            
            newConnexion = 



    def addRegularEntryHelper(self, dayOfWeek, uid, connexion):
        """
        Adds the specified regular connexion for specified train ID (tid) 
        and user ID (uid) at the singular day of week (mon, tue, wed, thu,
        fri, sat, sun).
        """
        assert dayOfWeek in self.validDays, dayOfWeek + " is not a valid day of week."

        if dayOfWeek == self.currentDayOfWeek: 
            # If dayOfWeek is today, have to add current travel to today's table
            self.todaysTable.addConnexionForDay(uid, connexion.tid, connexion)

        self.todaysTrainTable.addConnexion(connexion)
        self.regularTables[dayOfWeek].addConnexionForDay(uid, connexion.tid, connexion)


    def addSingularEntryHelper(self, dayOfYear, uid, connexion):
        """
        Adds the specified singular connexion for specified train ID (tid)
        and user ID (uid) at the singular day of year (1,...,365)
        """
        assert dayOfYear >= 0 and dayOfYear < 366, str(dayOfYear) + " is not a valid day expected: 0 <= dayOfYear < 366."

        if dayOfYear == self.currentDayOfYear: 
            # If dayOfYear is today, have to add current travel to today's table
            self.todaysTable.addConnexionForDay(uid, connexion.tid, connexion)


        if dayOfYear not in self.singularTables:
            self.singularTables[dayOfYear] = DayTable()

        self.todaysTrainTable.addConnexion(connexion)

        self.singularTables[dayOfYear].addConnexionForDay(uid, tid, connexion)


    def getRegularTableForDayOfWeek(self, dayOfWeek):
        """
        Returns the regular table for the specified day of the week.
        """
        assert dayOfWeek in self.validDays, dayOfWeek + " is not a valid day of week."
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
        assert currentDayOfWeek in self.validDays, currentDayOfWeek + " is not a valid day of week."
        assert currentDayOfYear >= 0 and currentDayOfYear < 366, str(currentDayOfYear) + " is not a valid day expected: 0 <= dayOfYear < 366."

        self.currentDayOfWeek = currentDayOfWeek
        self.currentDayOfYear = currentDayOfYear

        # Build today's tables:
        regularTable = self.regularTables[self.currentDayOfWeek]
        if self.currentDayOfYear in self.singularTables:
            singularTable = self.singularTables[self.currentDayOfYear]
        else:
            singularTable = DayTable()
        
        union = {**regularTable.getTable(), **singularTable.getTable()}
        self.todaysTable = DayTable(table=union)

        self.todaysTrainTable = TrainTable()
        for tid in self.todaysTable.table:
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


    def getTidsToCheck(self, currentTime, interval):
        """
        Returns all the tid of the trains that are more than +/- delay 
        from now.
        """
        tids = []
        for tid in self.todaysTrainTable:
            departureTime, arrivalTime = self.todaysTrainTable[tid]
            delayToNow = min(abs(currentTime - departureTime), abs(arrivalTime - currentTime))
            if(delayToNow > interval):
                tids.append(tid)


    def getUniqueConnexions(self, tids):
        """
        Returns unique connexions to check for current today's table.
        """
        uniqueConnexions = dict() # connexion, uids

        for tid in tids:
            for uid, connexion in self.todaysTable[tid]:
                if connexion not in uniqueConnexions:
                    uniqueConnexions[connexion] = [uid]
                else:
                    uniqueConnexions[connexions].append(uid)

        return uniqueConnexions