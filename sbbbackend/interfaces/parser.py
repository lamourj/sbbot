class Parser:
    @staticmethod
    def parseConnexion(connexion):
        def parseSections(sections):
            parsedSections = []
            size = len(sections)
            for s in sections:
                f = s['from']['location']['name']
                to = s['to']['location']['name']
                tdep = s['from']['debugHumanReadableTime']
                tarr = s['to']['debugHumanReadableTime']
                pdep = s['from']['platform']
                parr = s['to']['platform']
                route = s['route']
                t = route['name']
                i = route['infoName']
                strRoute = t + i
                dictSection = {'from': f, 'to': to, 'tid': strRoute, 'departureTime': tdep, 'arrivalTime': tarr, 'departurePlatform': pdep, 'arrivalPlatform': parr}
                parsedSections.append(dictSection)
            return parsedSections

        parsed = {}
        parsed['from'] = connexion['from']['location']['name']
        parsed['to'] = connexion['to']['location']['name']
        parsed['departureTime'] = connexion['from']['debugHumanReadableTime']
        parsed['arrivalTime'] = connexion['to']['debugHumanReadableTime']
        parsed['departurePlatform'] = connexion['from']['platform']
        parsed['arrivalPlatform'] = connexion['to']['platform']

        parsed['sections'] = [] + parseSections(connexion['sections'])
        return parsed


    @staticmethod
    def parseStations(stations):
        parsedStations = []
        for i in range(len(stations)):
            parsedStations.append(stations[i]['name'])
        return parsedStations
