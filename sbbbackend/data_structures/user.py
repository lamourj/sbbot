class User:
    """
        Class of User.
    """
    def __init__(self, uid):
        """ Create user with given userid. """
        self.uid = uid
        self.onetimes = []
        self.regulars = {}

    def addOneTimeConnexion(connexion):
        """ Add a one time connexion to this user. """
        if connexion not in self.onetimes:
            self.onetimes.append(connexion)

    def addRegularConnexion(connexion, day):
        """ Add a regular connexion to this user.
            day should be a string like "Monday", "Thuesday", ...
        """
        if day not in self.regulars:
            self.regulars[day] = [connexion]
        else:
            if connexion not in self.regulars[day]:
                self.regulars[day].append(connexion)