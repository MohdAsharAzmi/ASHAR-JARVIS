
import re


# =====================================
# ASHAR JARVIS - INDEPENDENT AGENTS V1
# =====================================


class GeneralAgent:

    def run(self, message="", **kwargs):
        return {
            "agent": "general",
            "status": "ready",
            "task": message,
            "message": "General Assistant is ready."
        }


# =====================================
# RESEARCH AGENT
# =====================================

class ResearchAgent:

    def run(self, task="", **kwargs):

        task = task.strip()

        if not task:
            raise ValueError("Research task cannot be empty")

        words = task.split()

        return {
            "agent": "research",
            "status": "offline_mode",
            "task": task,
            "analysis": {
                "topic": task,
                "word_count": len(words),
                "research_type": "general research"
            },
            "research_plan": [
                "Understand the research question",
                "Identify important subtopics",
                "Collect reliable information",
                "Compare available evidence",
                "Prepare a final report"
            ],
            "message": (
                "Research Agent has analysed your request. "
                "Live internet search is not connected yet. "
                "This agent is currently operating offline."
            )
        }


# =====================================
# CODING AGENT
# =====================================

class CodingAgent:

    def run(self, task="", **kwargs):

        task = task.strip()

        if not task:
            raise ValueError("Coding task cannot be empty")

        text = task.lower()

        languages = {
            "python": ["python", ".py"],
            "javascript": ["javascript", "js", ".js"],
            "html": ["html", ".html"],
            "css": ["css", ".css"],
            "java": ["java", ".java"],
            "c++": ["c++", "cpp"],
            "c": [" c ", "language c"]
        }

        detected_language = "not specified"

        for language, keywords in languages.items():
            if any(word in text for word in keywords):
                detected_language = language
                break

        if any(word in text for word in [
            "debug", "error", "bug", "fix", "problem"
        ]):
            task_type = "debugging"

            steps = [
                "Understand the reported problem",
                "Inspect the relevant code",
                "Identify the possible cause",
                "Prepare and test a correction"
            ]

        elif any(word in text for word in [
            "build", "create", "make", "develop", "website"
        ]):
            task_type = "project development"

            steps = [
                "Understand the project requirements",
                "Plan the project structure",
                "Identify required components",
                "Develop and test each component"
            ]

        elif any(word in text for word in [
            "explain", "meaning", "what is", "samjhao"
        ]):
            task_type = "code explanation"

            steps = [
                "Identify the programming concept",
                "Break it into smaller parts",
                "Explain its working",
                "Provide a simple example"
            ]

        else:
            task_type = "coding assistance"

            steps = [
                "Understand the coding request",
                "Identify the required programming concepts",
                "Prepare a solution plan",
                "Test the proposed approach"
            ]

        return {
            "agent": "coding",
            "status": "task_analysed",
            "task": task,
            "programming_language": detected_language,
            "task_type": task_type,
            "steps": steps,
            "message": (
                "Coding Agent analysed your request. "
                "Task type: " + task_type +
                ". Programming language: " + detected_language + "."
            )
        }


# =====================================
# CREATIVE AGENT
# =====================================

class CreativeAgent:

    def run(self, task="", media_type="image", **kwargs):

        task = task.strip()

        if not task:
            raise ValueError("Creative task cannot be empty")

        allowed_types = [
            "image", "video", "animation", "design"
        ]

        if media_type not in allowed_types:
            media_type = "image"

        return {
            "agent": "creative",
            "status": "concept_prepared",
            "task": task,
            "media_type": media_type,
            "creative_plan": [
                "Understand the creative idea",
                "Identify the visual style",
                "Plan the composition",
                "Define the required elements",
                "Prepare the final creative brief"
            ],
            "message": (
                "Creative Agent has prepared a "
                + media_type + " project plan. "
                "Generation tools are not connected yet."
            )
        }


# =====================================
# MEMORY AGENT
# =====================================

class MemoryAgent:

    def run(self, action="status", task="", **kwargs):

        text = (task or "").lower()

        if any(word in text for word in [
            "forget", "delete", "bhool jao", "hata do"
        ]):
            action = "forget"

        elif any(word in text for word in [
            "remember", "save", "yaad rakh", "yaad rakho"
        ]):
            action = "save"

        elif any(word in text for word in [
            "show memory", "list memory", "meri memory"
        ]):
            action = "list"

        return {
            "agent": "memory",
            "status": "not_connected",
            "action": action,
            "task": task,
            "message": (
                "Memory Agent identified the requested action: "
                + action +
                ". Permanent memory storage is our next development step."
            )
        }


# =====================================
# AGENT MANAGER
# =====================================

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
            raise TypeError(
                "Agent does not have a run method"
            )

        return agent.run(**kwargs)


# =====================================
# REGISTER ALL AGENTS
# =====================================

agent_manager = AgentManager()

agent_manager.register_agent("general", GeneralAgent())
agent_manager.register_agent("research", ResearchAgent())
agent_manager.register_agent("coding", CodingAgent())
agent_manager.register_agent("creative", CreativeAgent())
agent_manager.register_agent("memory", MemoryAgent())
