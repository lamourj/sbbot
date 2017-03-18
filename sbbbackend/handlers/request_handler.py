import requests
from .request_error import RequestError

class RequestHandler:
    """ Makes requests to the API using HTTPS. """

    def __init__(self, apikey):
        """ Create an handler with an api key. """
        self.apikey = apikey
        self.baseurl = "free.viapi.ch"

    def sendrequest(self, reqstring):
        """ Send request to the API.
            reqstring: request string in the form /XXX.
        """
        fullurl = "https://{}/v1{}".format(self.baseurl, reqstring)
        fullurl = fullurl + "&apiKeyWeb=" + self.apikey
        r = requests.get(fullurl)
        response = r.json()
        if r.status_code != 200:
            print(response)
            raise RequestError(response["status"], response["error"], response["message"])
        else:
            return response
