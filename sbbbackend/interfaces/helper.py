from .parser import Parser
from sbbbackend.handlers import QueryHandler

class Helper:
    qhandler = QueryHandler()

    @staticmethod
    def getOrElse(d, k, e):
        if k in d.keys():
            return str(d[k])
        else:
            return e

    @staticmethod
    def getConnexionsStrings(n, fromStation, toStation, viaStation=None, time=None, departure=True):
        response = Helper.qhandler.getConnexion(fromStation, toStation, viaStation, time, departure)
        connexions = response['connections'][:n]
        parsed = list(map(lambda x: Parser.parseConnexion(x), connexions))
    
        # Pretty print
        strings = []
        first = True
        for connexion in parsed:
            strings_for_connexion = []
            for c in connexion['sections']:
                s = ""
                if not first:
                    s = s + '\n'
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
                s = s +  ' '
                strings_for_connexion.append(s)
                first = False
            strings.append(strings_for_connexion)
        print(strings)
        return strings
