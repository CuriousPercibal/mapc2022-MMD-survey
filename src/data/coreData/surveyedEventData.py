from data.coreData.agentTarget import AgentTarget
from data.coreData.logisticTarget import LogisticTarget


class SurveyedEventData:
    target: LogisticTarget | AgentTarget

    def __init__(self, target: LogisticTarget | AgentTarget):
        self.target = target

    def __str__(self):
        return str({
            "target": self.target
        })