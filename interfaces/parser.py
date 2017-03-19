import datetime


class Parser:
    @staticmethod
    def parseConnexion(connexion, showSections=True):
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
                if route is not None:
                    t = route['name']
                    i = route['infoName']
                else:
                    continue
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

        sections = parseSections(connexion['sections'])
        if showSections:
            parsed['sections'] = sections

        if len(sections) > 0:
            parsed['tid'] = sections[0]['tid']
        else:
            parsed['tid'] = ''
        return parsed


    @staticmethod
    def parseStations(stations):
        parsedStations = []
        for i in range(len(stations)):
            parsedStations.append(stations[i]['name'])
        return parsedStations

    @staticmethod
    def parseHumanReadableTimeToMinutes(hrTime):
        parsed = hrTime.split()
        ampm = parsed[-1]
        parsed = parsed[1].split(':')
        minutes = int(parsed[0]) * 60 + int(parsed[1])
        if ampm == 'PM':
            minutes += 12*60
        return minutes

    @staticmethod
    def parseHumanReadableTimeToDayOfYear(hrTime):
        splitted = hrTime.split()
        month, day, year = splitted[0].split('/')
        day, month, year = int(day), int(month), int(year)
        dayOfYear = datetime.datetime(year, month, day, 10, 10, 10)
        return int(dayOfYear.strftime('%j')) - 1


    @staticmethod
    def millisToMinutes(millis):
        return millis / (1000 * 60)

    @staticmethod
    def minutesToMillis(minutes):
        return minutes * 1000 * 60