
import os


class BaseProvider:

    def generate(self, message, language, personality, history):
        raise NotImplementedError(
            "Provider must implement generate()"
        )


class OfflineProvider(BaseProvider):

    def generate(self, message, language, personality, history):

        return (
            "ASHAR JARVIS is currently in offline mode. "
            "Your message was received, but an AI model "
            "is not available right now."
        )


class GeminiProvider(BaseProvider):

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")

        self.model = os.getenv(
            "AI_MODEL",
            "gemini-2.5-flash"
        )

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing."
            )

    def generate(
        self,
        message,
        language="hinglish",
        personality="professional",
        history=None
    ):

        from google import genai
        from google.genai import types

        history = history or []

        system_instruction = (
            "You are ASHAR JARVIS, a professional personal AI assistant. "
            "Address the user as Ashar. "
            "Respond in: " + language + ". "
            "Personality: " + personality + ". "
            "Understand Hindi, English and Hinglish. "
            "Be accurate, clear and respectful. "
            "Never claim an action was completed unless it was."
        )

        contents = []

        for item in history[-10:]:

            if not isinstance(item, dict):
                continue

            text = (
                item.get("content")
                or item.get("message")
                or item.get("text")
                or ""
            )

            if not isinstance(text, str) or not text.strip():
                continue

            role = item.get("role", "user")

            if role in ("assistant", "model"):
                role = "model"
            else:
                role = "user"

            contents.append({
                "role": role,
                "parts": [{"text": text}]
            })

        contents.append({
            "role": "user",
            "parts": [{"text": message}]
        })

        try:

            client = genai.Client(
                api_key=self.api_key
            )

            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                    max_output_tokens=1500
                )
            )

            if not response.text:
                raise RuntimeError(
                    "The AI returned an empty response."
                )

            return response.text

        except Exception as error:

            print(
                "Gemini API error:",
                str(error)
            )

            raise RuntimeError(
                "Gemini is currently unavailable."
            ) from error


class OpenAICompatibleProvider(BaseProvider):

    def generate(
        self,
        message,
        language,
        personality,
        history
    ):

        raise RuntimeError(
            "OpenAI-compatible provider is not configured."
        )


def get_ai_provider():

    provider_name = os.getenv(
        "AI_PROVIDER",
        "offline"
    ).lower()

    if provider_name == "offline":
        return OfflineProvider()

    if provider_name == "gemini":
        return GeminiProvider()

    if provider_name == "openai":
        return OpenAICompatibleProvider()

    raise ValueError(
        "Unsupported AI provider: " + provider_name
    )


def get_provider_status():

    provider_name = os.getenv(
        "AI_PROVIDER",
        "offline"
    ).lower()

    model_name = os.getenv(
        "AI_MODEL",
        "not-selected"
    )

    if provider_name == "gemini":

        configured = bool(
            os.getenv("GEMINI_API_KEY")
        )

        return {
            "provider": "gemini",
            "model": model_name,
            "status": (
                "configured_not_tested"
                if configured
                else "missing_api_key"
            ),
            "real_ai_connected": False,
            "note": "API connectivity has not been tested."
        }

    if provider_name == "offline":

        return {
            "provider": "offline",
            "model": "independent",
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
