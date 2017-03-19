from .parser import Parser
from handlers import QueryHandler

class Helper:
    qhandler = QueryHandler()

    @staticmethod
    def getOrElse(d, k, e):
        if k in d.keys():
            return str(d[k])
        else:
            return e

    @staticmethod
    def getConnexionsStrings(connexions):
        parsed = list(map(lambda x: Parser.parseConnexion(x, False), connexions))
    
        # Pretty print
        strings = []
        first = True
        for c in parsed:
            s = ""
            s = s +  c['departureTime']
            s = s +  ' ' 
            if c['tid'] is not None:
                s = s +  c['tid']
            s = s +  ' : ' 
            s = s +  c['from']
            if c['departurePlatform'] is not None:
                s = s +  " plt. " 
                s = s +  c['departurePlatform'] 
            s = s +  ' to ' 
            s = s +  c['to'] 
            if c['arrivalPlatform'] is not None:
                s = s +  " plt. " 
                s = s +  c['arrivalPlatform'] 
            s = s +  ' ' 
            s = s +  c['arrivalTime'] 
            strings.append([s])
        return strings
