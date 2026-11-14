
import os
import re

from core.agents import agent_manager
from core.providers import (
    get_ai_provider,
    OfflineProvider
)


AGENT_KEYWORDS = {

    "research": [
        "research", "search", "internet",
        "find information", "look up",
        "maloomat", "talash", "khojo",
        "jaankari", "jankari",
        "kis bare mein", "ke baare mein batao",
        "importance", "benefits",
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
        "code banao", "variables",
        "functions", "loops", "classes",
        "syntax", "algorithm"
    ],

    "creative": [
        "image", "photo", "picture",
        "video", "animation",
        "generate image", "edit image",
        "tasveer", "design", "poster",
        "thumbnail", "logo", "interface",
        "ui design"
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

    # MEMORY PRIORITY
    memory_terms = [
        "remember", "save this",
        "forget", "memory",
        "yaad rakho", "yaad rakh",
        "bhool jao", "save kar lo",
        "delete memory", "show memory",
        "meri memory"
    ]

    if any(term in text for term in memory_terms):
        return "memory"

    # CODING PRIORITY
    coding_terms = [
        "python", "javascript", "html",
        "css", "java", "c++",
        "programming", "coding",
        "code", "debug", "variables",
        "functions", "loops", "classes",
        "syntax", "algorithm",
        "program", "web development"
    ]

    if any(
        re.search(
            r"\b" + re.escape(term) + r"\b",
            text
        )
        for term in coding_terms
    ):
        return "coding"

    # CREATIVE PRIORITY
    creative_terms = [
        "generate image", "edit image",
        "image", "photo", "picture",
        "video", "animation",
        "tasveer", "design", "poster",
        "thumbnail", "logo", "interface",
        "ui design"
    ]

    if any(term in text for term in creative_terms):
        return "creative"

    # NORMAL KEYWORD SCORING
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


def generate_general_reply(
    message,
    language,
    personality,
    history
):

    external_ai_allowed = (
        os.getenv(
            "ALLOW_EXTERNAL_AI",
            "false"
        ).lower() == "true"
    )

    provider_name = os.getenv(
        "AI_PROVIDER",
        "offline"
    ).lower()

    if external_ai_allowed:

        provider = get_ai_provider()

    else:

        provider = OfflineProvider()

    try:

        reply = provider.generate(
            message=message,
            language=language,
            personality=personality,
            history=history
        )

        return {
            "agent": "general",
            "status": (
                "ai_response"
                if external_ai_allowed and provider_name != "offline"
                else "offline_mode"
            ),
            "provider": (
                provider_name
                if external_ai_allowed
                else "offline"
            ),
            "message": reply
        }

    except Exception as error:

        print(
            "AI provider error:",
            str(error)
        )

        fallback = OfflineProvider()

        return {
            "agent": "general",
            "status": "offline_fallback",
            "provider": "offline",
            "message": fallback.generate(
                message,
                language,
                personality,
                history
            )
        }


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

            result = generate_general_reply(
                message=message,
                language=language,
                personality=personality,
                history=history
            )

        # CREATIVE AGENT
        elif selected_agent == "creative":

            text = message.lower()

            if any(word in text for word in [
                "animation", "animate"
            ]):

                media_type = "animation"

            elif any(word in text for word in [
                "video", "movie"
            ]):

                media_type = "video"

            elif any(word in text for word in [
                "design", "poster", "thumbnail",
                "interface", "ui", "logo"
            ]):

                media_type = "design"

            else:

                media_type = "image"

            result = agent_manager.run_agent(
                "creative",
                task=message,
                media_type=media_type
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

        print(
            "Brain processing error:",
            str(error)
        )

        return {
            "status": "error",
            "assistant": "ASHAR JARVIS",
            "selected_agent": selected_agent,
            "message": (
                "An error occurred while processing your request."
            )
        }
