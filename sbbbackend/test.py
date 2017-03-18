#!/bin/python3

from handlers import *

API_KEY = "V001CE953B0F-8B55-41EA-BD81-A366B72523BC"

def main():
    handler = RequestsHandler(API_KEY)
    print (handler.sendrequest("/stations?query=Z%C3%BCrich,%20C"))

if __name__ == '__main__':
    main()
