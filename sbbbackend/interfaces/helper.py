from .parser import Parser
from sbbbackend.handlers import QueryHandler

class Helper:
    qhandler = QueryHandler()

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
                s = s + c['tid'] + ' : ' + c['from'] + " plt. " + c['departurePlatform'] + ' ' + c['departureTime'] + '\n'
                s = s + 'to ' + c['to'] + " plt. " + c['arrivalPlatform'] + ' ' + c['arrivalTime'] + '\n'
                strings_for_connexion.append(s)
                first = False
            strings.append(strings_for_connexion)
        print(strings)
        return strings
        
