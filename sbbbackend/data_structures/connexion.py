class Connexion:
    """
        A connexion between 2 stops.
    """
    def __init__(self, departure, arrival, tid):
        self.departure = departure
        self.arrival = arrival
        self.tid = tid
