class RequestError(Exception):
    """ Custom exception class for error returned by the API. """

    def __init__(self, errcode, error, longmessage):
        """ Construct the error with the given error code and message. """
        self.errcode = errcode
        self.error = error
        super(RequestError, self).__init__(longmessage)
