class Parser:
    @staticmethod
    def parseConnexion(connexion):
        def parseSections(sections):
            parsedSections = []
            size = len(sections)
            for s in sections:
                f = s['from']['location']['name']
                to = s['to']['location']['name']
                route = s['route']
                t = route['name']
                i = route['infoName']
                strRoute = t + i
                dictSection = {'from': f, 'to': to, 'tid': strRoute}
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


    @staticmethod
    def parseHumanReadableTime(hrTime):
        parsed = hrTime.split()
        ampm = parsed[-1]
        parsed = parsed[1].split(':')
        minutes = int(parsed[0]) * 60 + int(parsed[1])
        if ampm == 'PM':
            minutes += 12*60

        return minutes

    @staticmethod
    def millisToMinutes(millis):
        return millis * 1000 * 60