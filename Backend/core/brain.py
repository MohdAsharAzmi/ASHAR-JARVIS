
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

    agent = agent_manager.get_agent("general")

    if agent is None:
        return "JARVIS agent is unavailable."

    return agent_manager.run_agent(
    "general",
    message=message,
    language=language,
    personality=personality,
    history=history
    )
