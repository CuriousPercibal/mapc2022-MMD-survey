import random

from agent.action import AgentAction, MoveAction, DetachAction
from agent.action.surveyAction import SurveyAction
from agent.intention import AdoptRoleIntention, DetachBlocksIntention, TravelIntention, MainAgentIntention
from agent.intention.explorerIntentions import ExploreIntention
from data.coreData import MapValueEnum, EventType, Coordinate, Direction
from data.coreData.logisticTarget import LogisticTarget
from data.coreData.surveyedEventData import SurveyedEventData
from data.intention import Observation


class SurveyIntention(ExploreIntention):
    surveyed: bool
    detachBlocksIntention: DetachBlocksIntention | None
    adoptRoleIntention: AdoptRoleIntention | None
    relocation: bool  # Contains if the Agent not found a close unknown Coordinate so
    triedDirections: set

    # it will move to a random location

    def __init__(self) -> None:
        self.id = random.randint(0, 10000)
        self.surveyed = False
        self.currentTravelIntention = None
        self.detachBlocksIntention = None
        self.adoptRoleIntention = None
        self.relocation = False
        self.prevDistance = 100.0
        self.currentSurveyTarget = MapValueEnum.GOAL
        self.triedDirections = set()
        self.lastDirection = Direction.NORTH
        self.goals = {"goal", "dispenser"}
        self.lastGoal = "goal"

    def getPriority(self) -> float:
        return 6.5

    async def planNextAction(self, observation: Observation) -> AgentAction:
        if len(self.goals) == 0:
            return await super().planNextAction(observation)

        surveyEvents = list(filter(lambda event: EventType.isSurveyed(event.type), observation.agentData.dynamicPerceptWrapper.events))
        # print(f"Survey events: {surveyEvents}")
        # print(f"Events: {list(map(lambda x: str(x), observation.agentData.dynamicPerceptWrapper.events))}")

        # if len(observation.agentData.attachedEntities) > 0:
        #     agentData = observation.agentData
        #     entity = observation.agentData.attachedEntities[0]
        #     direction = Coordinate.getDirection(observation.map.getAgentCoordinate(agentData.id), entity.relCoord)
        #     print(f"Detach entity: {entity.details}")
        #     return DetachAction(direction)

        if len(surveyEvents) > 0:
            surveyEventData = surveyEvents[0].data
            print(f"{observation.agentData.id} processes survey data: {surveyEventData}")

            if type(surveyEventData) == SurveyedEventData and type(surveyEventData.target) == LogisticTarget:
                currentDistance = surveyEventData.target.distance

                if self.prevDistance < currentDistance:
                    self.triedDirections.add(self.lastDirection)

                    if len(self.triedDirections) >= 3:
                        self.triedDirections = {self.lastDirection}

                    directions = set([direction for direction in Direction])
                    availableMoves = directions - self.triedDirections
                    print(f"{observation.agentData.id} available moves: {availableMoves}")
                    self.lastDirection = random.choice(list(directions))
                    print(f"{observation.agentData.id} selected move: {self.lastDirection}")


                print(f"{observation.agentData.id} is moving towards goal: distance: {currentDistance}, direction: {self.lastDirection}, last: {self.lastDirection}")
                self.prevDistance = currentDistance
                moveDirection = [self.lastDirection for _ in range(2)]
                coords = observation.map.getAgentCoordinate(observation.agentData.id)
                coords.move(moveDirection)
                self.currentTravelIntention = TravelIntention(coords)

        print(f"{observation.agentData.id} has travel intention: {self.currentTravelIntention is not None}")
        if self.currentTravelIntention is None or self.currentTravelIntention.checkFinished(observation):
            if self.lastGoal not in self.goals:
                self.lastGoal = random.choice(list(self.goals))
            # self.surveyed = True
            return SurveyAction(self.lastGoal)

        print(f"{observation.agentData.id} is travelling {self.currentTravelIntention.explain()}")
        return await self.currentTravelIntention.planNextAction(observation)


    def checkFinished(self, observation: Observation) -> bool:
        agentCoord = observation.map.getAgentCoordinate(observation.agentData.id)
        print(f"Is {observation.agentData.id} Finished? {self.goals}")
        dispensers = observation.map.dispenserMap.dispensers.values()
        neighbours = agentCoord.getSurroundingNeighbors()
        dispenserCoords = [c  for b in list(dispensers) for c in b]
        anyDispenser = [a == b for a in dispenserCoords for b in neighbours]
        if any(anyDispenser):
            print(f"{observation.agentData.id} found dispenser. Removing")
            self.goals = self.goals - {"dispenser"}
        if agentCoord in observation.map.goalZones:
            print(f"{observation.agentData.id} found goal. Removing")
            self.goals = self.goals - {"goal"}
        if len(self.goals) == 0:
            return super().checkFinished(observation)
        return False

    def explain(self) -> str:
        if self.currentTravelIntention is not None:
            return f"survey to {self.lastGoal}"
        else:
            return "surveying to unknown"
