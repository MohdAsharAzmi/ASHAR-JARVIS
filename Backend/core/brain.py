
import re

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


# Connect General Agent to the AI Brain
agent_manager.register_agent(
    "general",
    GeneralAgent()
)


AGENT_KEYWORDS = {

    "research": [
        "research",
        "search",
        "internet",
        "find information",
        "look up",
        "maloomat",
        "talash",
        "khojo",
        "jaankari",
        "jankari",
        "kis bare mein",
        "ke baare mein batao"
    ],

    "coding": [
        "code",
        "coding",
        "program",
        "python",
        "javascript",
        "html",
        "css",
        "debug",
        "error",
        "bug",
        "website",
        "web development",
        "programming",
        "code likho",
        "code banao"
    ],

    "creative": [
        "image",
        "photo",
        "picture",
        "video",
        "animation",
        "generate image",
        "edit image",
        "tasveer",
        "design",
        "poster",
        "thumbnail"
    ],

    "memory": [
        "remember",
        "save this",
        "forget",
        "memory",
        "yaad rakh",
        "yaad rakho",
        "bhool jao",
        "save kar lo",
        "delete memory"
    ]
}


def count_matches(text, keywords):

    score = 0

    for keyword in keywords:

        if " " in keyword:
            if keyword in text:
                score += 2

        else:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                score += 1

    return score


def select_agent(message: str) -> str:

    text = message.lower().strip()

    scores = {}

    for agent_name, keywords in AGENT_KEYWORDS.items():

        scores[agent_name] = count_matches(
            text,
            keywords
        )

    best_agent = max(
        scores,
        key=scores.get
    )

    if scores[best_agent] == 0:
        return "general"

    return best_agent


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
    
