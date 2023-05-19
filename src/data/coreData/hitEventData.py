from data.coreData import Coordinate


class HitEventData:
    origin: Coordinate

    def __init__(self, origin: Coordinate):
        self.origin = origin