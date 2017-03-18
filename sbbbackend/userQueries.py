from urllib.request import quote as urlqt

class userQueries:
    """
    Returns queries to be submitted to viadi API
    """



    """
    Query that will return connexions corresponding to input. Also returns the queries to get
    nextRequest and prevRequest.
    Default value for time: now
    Set departure to False to arrive at the specified time, otherwise True to 
    depart at the specified time.
    Departure should only be false if time is specified.
    type(time)=long
    """
    def getConnexion(fromStation, toStation, viaStation=None, time=None, departure=True):
        base = "/connection?from=" + getStationsFromName(fromStation) + "&to=" + getStationsFromName(toStation)

        if(not (viaStation==None)):
            base += "&via=" + getStationsFromName(viaStation)
        if(not (time==None)):
            base += "&time=" + time
        if(not departure):
            assert (not time==None), "Departure should not be set to false if time is not set."
            base += "&departure=false"

        return base


    """
    Query that will return next departures from specified station.
    Default value for time: now.
    type(time)=long
    """
    def getDeparturesFromStation(fromStation, time=None):
        base = "/departures?from=" + getDeparturesFromStation(fromStation)

        if(not time==None):
            base += "&time=" + time

        return base


    """
    Query that will return some stations suggestions according to user input
    """
    def getStationsFromName(userInput):
        return "/stations?query=" + urlqt(userInput)