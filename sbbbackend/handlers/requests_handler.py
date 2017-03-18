import requests
from .request_error import RequestError

class RequestsHandler:
    """ Makes requests to the API using HTTPS. """

    def __init__(self, apikey):
        """ Create an handler with an api key. """
        self.apikey = apikey
        self.baseurl = "free.viapi.ch"

    def sendrequest(self, reqstring):
        """ Send requeste to the API.
            reqstring: request string in the form /XXX.
        """
        fullurl = "https://{}/v1{}".format(self.baseurl, reqstring)
        fullurl = fullurl + "&apiKeyWeb=" + self.apikey
        r = requests.get(fullurl)
        if r.status_code != 200:
            response = r.json()
            print (response)
            raise RequestError(response["status"], response["error"], response["message"])
        else:
            print("Success.")
