from urllib.request import quote as urlqt

""" Returns some stations suggestions
	according to user input
"""
def getStationsFromName(userInput):
	return "/v1/stations?query=" + urlqt(userInput)