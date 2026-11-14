
import os
import re

from core.memory_store import (
    save_memory,
    get_memories,
    search_memories,
    delete_memory
)

from core.providers import get_ai_provider


# =====================================
# GENERAL AGENT
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
            raise ValueError(
                "Research task cannot be empty"
            )

        return {
            "agent": "research",
            "status": "offline_mode",
            "task": task,

            "analysis": {
                "topic": task,
                "word_count": len(task.split()),
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
                "Research Agent analysed your request. "
                "Live internet search is not connected yet."
            )
        }


# =====================================
# CODING AGENT V3
# =====================================

class CodingAgent:

    def run(self, task="", **kwargs):

        task = task.strip()

        if not task:
            raise ValueError(
                "Coding task cannot be empty"
            )

        text = task.lower()

        # Detect programming language

        languages = {
            "python": ["python", ".py"],
            "javascript": ["javascript", ".js"],
            "html": ["html", ".html"],
            "css": ["css", ".css"],
            "java": ["java", ".java"],
            "c++": ["c++", "cpp"],
            "c": ["language c"]
        }

        detected_language = "not specified"

        for language, keywords in languages.items():

            if any(
                re.search(
                    r"\b" + re.escape(word) + r"\b",
                    text
                )
                for word in keywords
            ):

                detected_language = language
                break

        # Detect task type

        if any(word in text for word in [
            "debug", "error", "bug", "fix",
            "not working", "problem"
        ]):

            task_type = "debugging"

        elif any(word in text for word in [
            "explain", "meaning", "samjhao",
            "how does", "what is", "variables"
        ]):

            task_type = "code explanation"

        elif any(word in text for word in [
            "write code", "generate code",
            "code likho", "code banao"
        ]):

            task_type = "code generation"

        elif any(word in text for word in [
            "build", "create", "make",
            "develop", "website", "project"
        ]):

            task_type = "project development"

        else:

            task_type = "coding assistance"

        # Check external AI permission

        external_ai_allowed = (
            os.getenv(
                "ALLOW_EXTERNAL_AI",
                "false"
            ).lower() == "true"
        )

        provider_name = os.getenv(
            "AI_PROVIDER",
            "offline"
        ).lower()

        # Actual AI response

        if external_ai_allowed and provider_name != "offline":

            try:

                provider = get_ai_provider()

                prompt = (
                    "You are ASHAR JARVIS Coding Agent, "
                    "an expert programming tutor. "
                    "Understand the coding request. "
                    "Explain concepts with simple examples. "
                    "For debugging, explain the likely cause "
                    "and a safe correction. "
                    "For code generation, provide readable code. "
                    "Prefer step-by-step guidance. "
                    "Use Hindi, English or Hinglish naturally. "
                    "Do not claim code was tested unless it was. "
                    "Programming language: "
                    + detected_language
                    + ". Task type: "
                    + task_type
                    + ". User request: "
                    + task
                )

                answer = provider.generate(
                    message=prompt,
                    language="hinglish",
                    personality="professional",
                    history=[]
                )

                return {
                    "agent": "coding",
                    "status": "ai_response",
                    "programming_language": detected_language,
                    "task_type": task_type,
                    "answer": answer,
                    "message": (
                        "Coding Agent V3 generated an AI response."
                    )
                }

            except Exception as error:

                print(
                    "Coding Agent AI error:",
                    str(error)
                )

        # Offline guidance

        guidance = {

            "debugging": [
                "Inspect the error message",
                "Check the relevant code",
                "Identify the possible cause",
                "Prepare and verify a correction"
            ],

            "code explanation": [
                "Identify the programming concept",
                "Understand its purpose",
                "Break it into smaller parts",
                "Study a simple example"
            ],

            "code generation": [
                "Understand the desired output",
                "Identify the programming language",
                "Plan the code structure",
                "Prepare and test the code"
            ],

            "project development": [
                "Understand project requirements",
                "Plan the project structure",
                "Identify required technologies",
                "Build components step by step",
                "Test the completed project"
            ],

            "coding assistance": [
                "Understand the coding request",
                "Identify relevant concepts",
                "Prepare a solution approach",
                "Test the proposed solution"
            ]
        }

        return {
            "agent": "coding",
            "status": "offline_guidance",
            "task": task,
            "programming_language": detected_language,
            "task_type": task_type,
            "guidance": guidance[task_type],
            "message": (
                "Coding Agent V3 analysed your request. "
                "External AI is disabled, so detailed "
                "AI-generated coding assistance is unavailable."
            )
        }


# =====================================
# CREATIVE AGENT
# =====================================

class CreativeAgent:

    def run(self, task="", media_type="image", **kwargs):

        task = task.strip()

        if not task:
            raise ValueError(
                "Creative task cannot be empty"
            )

        allowed_types = [
            "image",
            "video",
            "animation",
            "design"
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
                "Define required elements",
                "Prepare the creative brief"
            ],

            "message": (
                "Creative Agent prepared a "
                + media_type
                + " project plan. "
                "Generation tools are not connected yet."
            )
        }


# =====================================
# MEMORY AGENT
# =====================================

class MemoryAgent:

    def run(self, action="status", task="", **kwargs):

        task = (task or "").strip()
        text = task.lower()

        # SAVE MEMORY

        if text.startswith((
            "save:",
            "remember:",
            "yaad rakho:"
        )):

            content = task.split(":", 1)[1].strip()

            if not content:
                raise ValueError(
                    "Memory content is empty"
                )

            result = save_memory(content)

            return {
                "agent": "memory",
                "status": "saved",
                "memory": result,
                "message": "Memory successfully saved."
            }

        # SEARCH MEMORY

        if text.startswith((
            "search:",
            "find:"
        )):

            query = task.split(":", 1)[1].strip()

            results = search_memories(query)

            return {
                "agent": "memory",
                "status": "search_completed",
                "results": results,
                "message": "Memory search completed."
            }

        # LIST MEMORIES

        if text in (
            "list",
            "show",
            "show all",
            "list memories"
        ):

            results = get_memories()

            return {
                "agent": "memory",
                "status": "retrieved",
                "total": len(results),
                "memories": results,
                "message": "Saved memories retrieved."
            }

        # DELETE MEMORY

        if text.startswith("delete:"):

            memory_id = task.split(":", 1)[1].strip()

            if not memory_id.isdigit():
                raise ValueError(
                    "Provide a valid memory ID"
                )

            deleted = delete_memory(
                int(memory_id)
            )

            return {
                "agent": "memory",
                "status": (
                    "deleted" if deleted else "not_found"
                ),
                "memory_id": int(memory_id),
                "message": (
                    "Memory deleted."
                    if deleted
                    else "Memory ID not found."
                )
            }

        return {
            "agent": "memory",
            "status": "waiting_for_command",

            "supported_commands": [
                "save: your information",
                "search: keyword",
                "list",
                "delete: memory_id"
            ],

            "message": (
                "Please use a supported memory command."
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
            raise ValueError(
                "Agent not found: " + name
            )

        if not hasattr(agent, "run"):
            raise TypeError(
                "Agent does not have a run method"
            )

        return agent.run(**kwargs)


# =====================================
# REGISTER ALL AGENTS
# =====================================

agent_manager = AgentManager()

agent_manager.register_agent(
    "general",
    GeneralAgent()
)

agent_manager.register_agent(
    "research",
    ResearchAgent()
)

agent_manager.register_agent(
    "coding",
    CodingAgent()
)

agent_manager.register_agent(
    "creative",
    CreativeAgent()
)

agent_manager.register_agent(
    "memory",
    MemoryAgent()
)
