class Connexion:
    """
        A connexion between 2 stops.
    """
    def __init__(self, tid, departure, arrival, departureTime, arrivalTime, departurePlatform, arrivalPlatform):
        self.departure = departure
        self.arrival = arrival
        self.tid = tid
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.departurePlatform = departurePlatform
        self.arrivalPlatform = arrivalPlatform
