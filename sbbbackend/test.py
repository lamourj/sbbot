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

if __name__ == '__main__':
    main()
