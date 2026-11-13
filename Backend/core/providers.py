
import os
from google import genai
from google.genai import types


class BaseProvider:

    def generate(self, message, language, personality, history):
        raise NotImplementedError(
            "Provider must implement generate()"
        )


class DemoProvider(BaseProvider):

    def generate(self, message, language, personality, history):
        return (
            "JARVIS received your message: "
            + message
            + ". Demo AI is active."
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
        language,
        personality,
        history
    ):

        system_instruction = (
            "You are ASHAR JARVIS, a professional personal AI assistant. "
            "Address the user as Ashar. "
            "Respond in the requested language: " + language + ". "
            "Your personality should be: " + personality + ". "
            "You can understand Hindi, English and Hinglish. "
            "Be helpful, accurate, clear and respectful. "
            "Never pretend to have performed an action you did not perform."
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
            with genai.Client(
                api_key=self.api_key
            ) as client:

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
                return "I couldn't generate a response. Please try again."

            return response.text

        except Exception as error:
            print("Gemini API error:", str(error))

            raise RuntimeError(
                "Gemini request failed. Check API key, model, quota and connection."
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
        "demo"
    ).lower()

    if provider_name == "demo":
        return DemoProvider()

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
        "demo"
    ).lower()

    model_name = os.getenv(
        "AI_MODEL",
        "gemini-2.5-flash"
    )

    if provider_name == "gemini":

        configured = bool(
            os.getenv("GEMINI_API_KEY")
        )

        return {
            "provider": "gemini",
            "model": model_name,
            "status": (
                "configured" if configured else "missing_api_key"
            ),
            "real_ai_connected": False
        }

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
