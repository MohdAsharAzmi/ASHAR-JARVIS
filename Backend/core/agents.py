
class GeneralAgent:
    def run(self, **kwargs):
        return {"agent": "general", "status": "ready"}



class ResearchAgent:
    def run(self, task: str = "", **kwargs):
        task = task.strip()

        if not task:
            raise ValueError("Research task cannot be empty")

        return {
            "agent": "research",
            "status": "planning",
            "task": task,
            "research_plan": {
                "objective": (
                    "Understand the topic and prepare "
                    "a structured research report."
                ),
                "questions": [
                    "What is the topic?",
                    "Why is it important?",
                    "What are its main facts?",
                    "What are its effects or applications?"
                ],
                "report_sections": [
                    "Introduction",
                    "Key Information",
                    "Importance",
                    "Conclusion"
                ]
            },
            "sources": [],
            "message": (
                "Research plan created. "
                "Internet search is not connected yet."
            )
        }



class CodingAgent:
    def run(self, task: str = "", **kwargs):
        return {
            "agent": "coding",
            "status": "registered",
            "task": task,
            "message": "Coding capabilities are not connected yet."
        }


class CreativeAgent:
    def run(self, task: str = "", media_type: str = "image", **kwargs):
        return {
            "agent": "creative",
            "status": "registered",
            "task": task,
            "media_type": media_type,
            "message": "Creative models are not connected yet."
        }


class MemoryAgent:
    def run(self, action: str = "status", **kwargs):
        return {
            "agent": "memory",
            "status": "registered",
            "action": action,
            "message": "Persistent memory storage is not connected yet."
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
            raise ValueError("Agent not found: " + name)

        if not hasattr(agent, "run"):
            raise TypeError("Agent does not have a run method")

        return agent.run(**kwargs)


agent_manager = AgentManager()

agent_manager.register_agent("general", GeneralAgent())
agent_manager.register_agent("research", ResearchAgent())
agent_manager.register_agent("coding", CodingAgent())
agent_manager.register_agent("creative", CreativeAgent())
agent_manager.register_agent("memory", MemoryAgent())
