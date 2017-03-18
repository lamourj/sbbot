class Connexion:
    """
        A connexion between 2 stops.
    """
    def __init__(self, departure, arrival, trainid):
        self.departure = departure
        self.arrival = arrival
        self.trainid = trainid
