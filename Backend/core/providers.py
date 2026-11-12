
import os


class DemoProvider:

    def generate(
        self,
        message: str,
        language: str,
        personality: str,
        history: list
    ) -> str:

        return (
            "JARVIS received your message: "
            + message
            + ". Language: "
            + language
            + ". Personality: "
            + personality
            + ". Previous messages: "
            + str(len(history))
            + ". AI model is not connected yet."
        )


def get_ai_provider():

    provider_name = os.getenv(
        "AI_PROVIDER",
        "demo"
    ).lower()

    if provider_name == "demo":
        return DemoProvider()

    raise ValueError(
        "Unsupported AI provider: " + provider_name
    )
  
