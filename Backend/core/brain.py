
import re
from core.agents import agent_manager


AGENT_KEYWORDS = {

"research": [
    "research", "search", "internet",
    "find information", "look up",
    "maloomat", "talash", "khojo",
    "jaankari", "jankari",
    "kis bare mein", "ke baare mein batao",
    "explain", "importance", "benefits",
    "causes", "history", "facts",
    "tell me about", "what is",
    "how does", "why is",
    "describe", "advantages",
    "disadvantages"
],


    "coding": [
        "code", "coding", "program",
        "python", "javascript", "html",
        "css", "debug", "error", "bug",
        "website", "web development",
        "programming", "code likho",
        "code banao"
    ],

    "creative": [
        "image", "photo", "picture",
        "video", "animation",
        "generate image", "edit image",
        "tasveer", "design", "poster",
        "thumbnail"
    ],

    "memory": [
        "remember", "save this",
        "forget", "memory",
        "yaad rakh", "yaad rakho",
        "bhool jao", "save kar lo",
        "delete memory", "show memory",
        "meri memory"
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


def select_agent(message):
    text = message.lower().strip()

    scores = {}

    for agent_name, keywords in AGENT_KEYWORDS.items():
        scores[agent_name] = count_matches(
            text,
            keywords
        )

    best_agent = max(scores, key=scores.get)

    if scores[best_agent] == 0:
        return "general"

    return best_agent


def generate_reply(
    message,
    language="hinglish",
    personality="professional",
    history=None
):

    message = message.strip()
    history = history or []

    if not message:
        return {
            "status": "error",
            "message": "Please tell me something."
        }

    selected_agent = select_agent(message)

    try:

        # GENERAL AGENT
        if selected_agent == "general":

            result = agent_manager.run_agent(
                "general",
                message=message,
                language=language,
                personality=personality,
                history=history
            )

        # SPECIALIST AGENTS
        else:

            result = agent_manager.run_agent(
                selected_agent,
                task=message
            )

        return {
            "status": "success",
            "assistant": "ASHAR JARVIS",
            "selected_agent": selected_agent,
            "language": language,
            "result": result,
            "message": result.get(
                "message",
                "Task processed successfully."
            )
        }

    except Exception as error:

        return {
            "status": "error",
            "assistant": "ASHAR JARVIS",
            "selected_agent": selected_agent,
            "message": "An error occurred while processing your request.",
            "error": str(error)
        }
        
