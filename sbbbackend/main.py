#!/bin/python3

from handlers import *
from data_structures import *
from interfaces import *
from datetime import datetime


def main():
    # init tables to store stuff
    tablesManager = TablesManager('sun', 77)

    
    betweenChecks = 1 * 60 * 1000 # 1 minute millis
    prevChecked = datetime.now().microsecond
    deleteAfterMinutes = 30
    checkIntervalMinutes = 120 # 2 hours
    notificationMinutes = 5

    while(True):
        currentTime = datetime.now().microsecond
        if(currentTime - prevChecked > betweenChecks):
            tablesManager.removePastTrains(Parser.millisToMinutes(currentTime), deleteAfterMinutes)
            tidsToCheck = tablesManager.getTidsToCheck(currentTime, checkIntervalMinutes)

    #       uniqueConnexions = tablesManager.getUniqueConnexions(tidsToCheck)
    #       for connexion, uids in uniqueConnexions:
    #           Query SBB to check connexion. 
    #           for problematicConnexions:
    #               for uid in uids:
    #                   inform uid about problem.

    #           if(Parser.millisToMinutes(currentTime) - connexion.departureTime == -notificationMinutes):
    #               for uid in uids:
    #                   inform uid about train leaving in 5 minutes

                    

    
    

if __name__ == '__main__':
    main()