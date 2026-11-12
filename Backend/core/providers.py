
import os


class BaseProvider:

    def generate(
        self,
        message,
        language,
        personality,
        history
    ):
        raise NotImplementedError(
            "Provider must implement generate()"
        )


class DemoProvider(BaseProvider):

    def generate(
        self,
        message,
        language,
        personality,
        history
    ):
        return (
            "JARVIS received your message: "
            + message
            + ". Language: "
            + language
            + ". Personality: "
            + personality
            + ". Previous messages: "
            + str(len(history))
            + ". Demo AI is active. Real model is not connected yet."
        )


class OpenAICompatibleProvider(BaseProvider):

    def __init__(self):
        self.model = os.getenv(
            "AI_MODEL",
            "not-selected"
        )

    def generate(
        self,
        message,
        language,
        personality,
        history
    ):
        raise RuntimeError(
            "AI provider is not activated yet. "
            "Provider configuration and authorization are required."
        )


def get_ai_provider():

    provider_name = os.getenv(
        "AI_PROVIDER",
        "demo"
    ).lower()

    if provider_name == "demo":
        return DemoProvider()

    if provider_name == "openai":
        return OpenAICompatibleProvider()

    raise ValueError(
        "Unsupported AI provider: " + provider_name
    )
    
