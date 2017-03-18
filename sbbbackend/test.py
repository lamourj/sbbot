#!/bin/python3

from handlers import *
from interfaces import *

API_KEY = "V001CE953B0F-8B55-41EA-BD81-A366B72523BC"

def main():
    handler = QueryHandler()
    json = handler.getConnexion("Aigle", "Zürich")
    json = handler.getStationsFromName("Zürich")
    # print(json)
    print(Parser.parseStations(json))

    # print(json)

    # connexion = json['connections'][0]
    # parsed = Parser.parseConnexion(connexion)
    # print(parsed)

if __name__ == '__main__':
    main()