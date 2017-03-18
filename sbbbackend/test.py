#!/bin/python3

from handlers import *

API_KEY = "V001CE953B0F-8B55-41EA-BD81-A366B72523BC"

def main():
    handler = QueriesHandler()
    print (handler.getConnexion("Lausanne", "Renens VD"))

if __name__ == '__main__':
    main()
