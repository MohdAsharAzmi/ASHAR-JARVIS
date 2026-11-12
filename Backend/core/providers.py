
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
            "AI provider is not activated yet."
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


def get_provider_status():

    provider_name = os.getenv(
        "AI_PROVIDER",
        "demo"
    ).lower()

    model_name = os.getenv(
        "AI_MODEL",
        "not-selected"
    )

    if provider_name == "demo":
        return {
            "provider": "demo",
            "model": "demo-model",
            "status": "active",
            "real_ai_connected": False
        }

    if provider_name == "openai":
        return {
            "provider": "openai",
            "model": model_name,
            "status": "configuration_only",
            "real_ai_connected": False
        }

    return {
        "provider": provider_name,
        "model": model_name,
        "status": "unsupported",
        "real_ai_connected": False
    }
    
