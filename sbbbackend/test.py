#!/bin/python3

from handlers import *
from interfaces import *

API_KEY = "V001CE953B0F-8B55-41EA-BD81-A366B72523BC"

def main():
    helper = Helper() 
    strings = helper.getConnexionsStrings(2, "Aigle", "Zürich")

    for ss in strings:
        print ('###########')
        for s in ss:
            print(s)
    # connexion = json['connections'][0]
    # parsed = Parser.parseConnexion(connexion)
    # print(parsed)

    someTime = "3/18/17 7:20 PM"
    correctTime, parsedTime = 19*60+20, Parser.parseHumanReadableTime(someTime)
    if not correctTime == parsedTime:
        print("NOOB")
    else:
        print("Hehehehhe")

if __name__ == '__main__':
    main()
