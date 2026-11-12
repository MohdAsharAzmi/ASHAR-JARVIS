
from core.providers import get_ai_provider
from core.agents import agent_manager


class GeneralAgent:

    def run(
        self,
        message,
        language,
        personality,
        history
    ):
        provider = get_ai_provider()

        return provider.generate(
            message=message,
            language=language,
            personality=personality,
            history=history
        )


# Register the general agent
agent_manager.register_agent(
    "general",
    GeneralAgent()
)


def select_agent(message: str) -> str:

    text = message.lower()

    # Research tasks
    research_words = [
        "research", "search", "internet",
        "find information", "look up",
        "maloomat", "talash", "khojo"
    ]

    # Coding tasks
    coding_words = [
        "code", "coding", "program",
        "python", "javascript", "html",
        "css", "debug", "error", "bug"
    ]

    # Creative tasks
    creative_words = [
        "image", "photo", "picture",
        "video", "animation", "generate image",
        "tasveer"
    ]

    # Memory tasks
    memory_words = [
        "remember", "save this",
        "forget", "memory",
        "yaad rakh", "bhool jao"
    ]

    if any(word in text for word in research_words):
        return "research"

    if any(word in text for word in coding_words):
        return "coding"

    if any(word in text for word in creative_words):
        return "creative"

    if any(word in text for word in memory_words):
        return "memory"

    return "general"


def generate_reply(
    message: str,
    language: str = "hinglish",
    personality: str = "professional",
    history: list = None
) -> str:

    message = message.strip()
    history = history or []

    if not message:
        return "Please tell me something."

    selected_agent = select_agent(message)

    # General conversation
    if selected_agent == "general":
        return agent_manager.run_agent(
            "general",
            message=message,
            language=language,
            personality=personality,
            history=history
        )

    # Specialist agent execution
    result = agent_manager.run_agent(
        selected_agent,
        task=message
    )

    return (
        "JARVIS selected the "
        + selected_agent
        + " agent. "
        + result.get(
            "message",
            "This agent is registered but its full capabilities are not connected yet."
        )
    )
    
