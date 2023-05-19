from data.coreData import EventType, Coordinate, MapValueEnum
from data.coreData.agentTarget import AgentTarget
from data.coreData.hitEventData import HitEventData
from data.coreData.logisticTarget import LogisticTarget
from data.coreData.surveyedEventData import SurveyedEventData


class Event:
    type: EventType
    data: HitEventData | SurveyedEventData

    def __init__(self, perception: dict, target: MapValueEnum):
        self.type = EventType.from_str(perception["type"])
        if self.type == EventType.SURVEYED:
            if target in [MapValueEnum.GOAL, MapValueEnum.ROLE, MapValueEnum.DISPENSER]:
                self.data = SurveyedEventData(LogisticTarget(target, perception["distance"]))
            if target == MapValueEnum.AGENT:
                self.data = SurveyedEventData(
                    AgentTarget(target, perception["name"], perception["role"], perception["energy"]))

        elif self.type == EventType.HIT:
            origin = perception["origin"]
            self.data = HitEventData(Coordinate(origin[0], origin[1]))

    def __str__(self):
        return f"type: {self.type}, data: [{self.data}]"
