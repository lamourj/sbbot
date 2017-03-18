class Connexion:
    """
        A connexion between 2 stops.
    """
    def __init__(self, tid, departure, arrival, departureTime, arrivalTime):
        self.departure = departure
        self.arrival = arrival
        self.tid = tid
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime