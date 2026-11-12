
from core.providers import get_ai_provider


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

    # Select the AI provider
    provider = get_ai_provider()

    # Generate response
    reply = provider.generate(
        message=message,
        language=language,
        personality=personality,
        history=history
    )

    return reply
