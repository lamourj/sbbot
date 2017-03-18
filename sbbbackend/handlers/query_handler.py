from urllib.request import quote as urlqt
from .request_handler import RequestHandler

class QueriesHandler:
    """
    Returns queries to be submitted to viadi API
    """

    def __init__(self):
        # TODO : Pass key as arg 
        apikey = "V001CE953B0F-8B55-41EA-BD81-A366B72523BC"
        self.reqhandler = RequestHandler(apikey)


    """
    Query that will return connexions corresponding to input. Also returns the queries to get
    nextRequest and prevRequest.
    Default value for time: now
    Set departure to False to arrive at the specified time, otherwise True to 
    depart at the specified time.
    Departure should only be false if time is specified.
    type(time)=long
    """
    def getConnexion(self, fromStation, toStation, viaStation=None, time=None, departure=True):
        base = "/connection?from=" + fromStation + "&to=" + toStation

        if viaStation is not None:
            base += "&via=" + viaStation
        if time is not None:
            base += "&time=" + time
        if not departure:
            assert time is not None, "Departure should not be set to false if time is not set."
            base += "&departure=false"

        return self.reqhandler.sendrequest(base)


    """
    Query that will return next departures from specified station.
    Default value for time: now.
    type(time)=long
    """
    def getDepartures(self, fromStation, time=None):
        base = "/departures?from=" + fromStation

        if time is not None:
            base += "&time=" + time

        return self.reqhandler.sendrequest(base)


    """
    Query that will return some stations suggestions according to user input
    """
    def getStationsFromName(self, userInput):
        return self.reqhandler.sendrequest("/stations?query=" + urlqt(userInput))
