from data.coreData import MapValueEnum


class AgentTarget:
    type: MapValueEnum
    name: str
    role: str
    energy: float

    def __init__(self, type: MapValueEnum, name: str, role: str, energy: float):
        self.type = type
        self.name = name
        self.role = role
        self.energy = energy

    def __str__(self):
        return str({
            "type": self.type,
            "name": self.name,
            "role": self.role,
            "energy": self.energy
        })
