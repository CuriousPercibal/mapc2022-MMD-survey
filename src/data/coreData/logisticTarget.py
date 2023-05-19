from data.coreData import MapValueEnum


class LogisticTarget:
    type: MapValueEnum
    distance: float

    def __init__(self, type: MapValueEnum, distance: float):
        self.type = type
        self.distance = distance

    def __str__(self):
        return str({
            "type": self.type,
            "distance": self.distance
        })