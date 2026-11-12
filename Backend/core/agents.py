
class GeneralAgent:

    def run(self, **kwargs):
        return {
            "agent": "general",
            "status": "ready"
        }


class ResearchAgent:

    def run(self, task: str = "", **kwargs):
        return {
            "agent": "research",
            "status": "registered",
            "task": task,
            "message": "Research capabilities are not connected yet."
        }


class AgentManager:

    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent):
        self.agents[name] = agent

    def get_agent(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())

    def run_agent(self, name, **kwargs):
        agent = self.get_agent(name)

        if agent is None:
            raise ValueError(
                "Agent not found: " + name
            )

        if not hasattr(agent, "run"):
            raise TypeError(
                "Agent does not have a run method"
            )

        return agent.run(**kwargs)


agent_manager = AgentManager()

agent_manager.register_agent(
    "general",
    GeneralAgent()
)

agent_manager.register_agent(
    "research",
    ResearchAgent()
)
