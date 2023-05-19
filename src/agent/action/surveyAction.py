from mapc2022 import Agent as MapcAgent, AgentActionError as MapcAgentActionError

from agent.action.agentAction import AgentAction

class SurveyAction(AgentAction):
    """
    Submits a `Task`, turning in the given attached `Blocks`.
    Only performable if the current `Agent` role can perform this action.\n
    Note that if the `Blocks` types and relative positions not match the
    `Task` requirements or if it is expired (passed the deadline or
    removed from the active tasks) then it will fail.
    """

    target: str

    def __init__(self, target: str) -> None:
        self.target = target

    def perform(self, agent: MapcAgent) -> str:
        """
        Sends the submit action to the simulation server
        and returns the result of it.
        If succeeded the 'submitted' `Blocks` disappear from
        the simulation.
        """

        try:
            print("Sending survey action")
            agent.survey(self.target)
            return "success"
        except MapcAgentActionError as e:
            return e.args[0]